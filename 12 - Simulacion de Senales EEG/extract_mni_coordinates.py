#!/usr/bin/env python3
"""
Extract MNI coordinates from FreeSurfer Destrieux Atlas + Subcortical Structures
Author: Claude
Date: 2026-02-27

This script extracts MNI coordinates for:
- All Destrieux atlas cortical regions (aparc.a2009s)
- Left and Right Hippocampus
- Left and Right Amygdala
"""

import numpy as np
import nibabel as nib
from nibabel.freesurfer import read_annot, read_geometry
import pandas as pd
import os
from pathlib import Path

# ==================== CONFIGURATION ====================
SUBJECT_DIR = Path("/Users/brainseeg/Documents/FreesurferStuffs/subjects/0391")
OUTPUT_FILE = Path.home() / "subject_0391_mni_coordinates.csv"

print("="*70)
print("FreeSurfer MNI Coordinate Extraction")
print("="*70)
print(f"Subject Directory: {SUBJECT_DIR}")
print(f"Output File: {OUTPUT_FILE}")
print("="*70)

# ==================== FUNCTIONS ====================

def read_talairach_xfm(xfm_file):
    """Read FreeSurfer talairach transformation matrix."""
    print(f"\n📐 Reading Talairach transformation: {xfm_file}")

    matrix = np.eye(4)
    with open(xfm_file, 'r') as f:
        lines = f.readlines()

    # Find the matrix in the file (skip header comments)
    matrix_lines = []
    reading_matrix = False
    for line in lines:
        if line.strip().startswith('Linear_Transform'):
            reading_matrix = True
            continue
        if reading_matrix and line.strip() and not line.strip().startswith('#'):
            if ';' in line:
                break
            matrix_lines.append(line.strip())

    # Parse the matrix
    if len(matrix_lines) >= 3:
        for i, line in enumerate(matrix_lines[:3]):
            values = [float(x) for x in line.split()]
            matrix[i, :] = values

    print("   Transformation matrix loaded ✓")
    return matrix

def apply_talairach_transform(coords, xfm_matrix):
    """Apply talairach transformation to coordinates."""
    # Convert to homogeneous coordinates
    coords_hom = np.column_stack([coords, np.ones(len(coords))])
    # Apply transformation
    mni_coords = coords_hom @ xfm_matrix.T
    return mni_coords[:, :3]

def extract_cortical_coordinates(subject_dir, hemi, xfm_matrix):
    """Extract MNI coordinates for all Destrieux regions in one hemisphere."""
    print(f"\n🧠 Processing {hemi.upper()} hemisphere cortical regions...")

    # File paths
    annot_file = subject_dir / "label" / f"{hemi}.aparc.a2009s.annot"
    surf_file = subject_dir / "surf" / f"{hemi}.pial.FLAIR"

    # If .FLAIR doesn't exist, try regular pial
    if not surf_file.exists():
        surf_file = subject_dir / "surf" / f"{hemi}.pial"

    print(f"   Annotation: {annot_file.name}")
    print(f"   Surface: {surf_file.name}")

    # Read annotation and surface
    labels, ctab, names = read_annot(annot_file)
    coords, faces = read_geometry(surf_file)

    print(f"   Vertices: {len(coords):,}")
    print(f"   Regions: {len(names)}")

    # Convert to MNI space
    mni_coords = apply_talairach_transform(coords, xfm_matrix)

    # Extract centroid for each region
    region_data = []
    for idx, region_name in enumerate(names):
        region_name_str = region_name.decode('utf-8') if isinstance(region_name, bytes) else region_name

        # Skip unknown/corpus callosum
        if 'unknown' in region_name_str.lower() or 'corpuscallosum' in region_name_str.lower():
            continue

        # Get vertices for this region
        vertex_mask = labels == idx
        n_vertices = vertex_mask.sum()

        if n_vertices == 0:
            continue

        # Compute centroid in MNI space
        region_mni_coords = mni_coords[vertex_mask]
        centroid = region_mni_coords.mean(axis=0)

        # Compute surface area (approximate)
        area_mm2 = n_vertices * 0.5  # Rough estimate, each vertex ~0.5mm²

        region_data.append({
            'Region_Name': region_name_str,
            'MNI_X': centroid[0],
            'MNI_Y': centroid[1],
            'MNI_Z': centroid[2],
            'Hemisphere': hemi.upper(),
            'N_Vertices': n_vertices,
            'Area_mm2': area_mm2,
            'Structure_Type': 'Cortical'
        })

    print(f"   Extracted {len(region_data)} regions ✓")
    return region_data

def extract_subcortical_coordinates(subject_dir, xfm_matrix):
    """Extract MNI coordinates for hippocampus and amygdala from aseg."""
    print(f"\n🔍 Processing subcortical structures (hippocampus, amygdala)...")

    aseg_file = subject_dir / "mri" / "aseg.mgz"
    print(f"   File: {aseg_file.name}")

    # Load aseg volume
    aseg_img = nib.load(aseg_file)
    aseg_data = aseg_img.get_fdata()
    affine = aseg_img.affine

    # FreeSurfer label IDs for structures of interest
    structures = {
        'Left-Hippocampus': 17,
        'Right-Hippocampus': 53,
        'Left-Amygdala': 18,
        'Right-Amygdala': 54
    }

    subcortical_data = []

    for name, label_id in structures.items():
        # Find voxels for this structure
        mask = aseg_data == label_id
        n_voxels = mask.sum()

        if n_voxels == 0:
            print(f"   ⚠️  {name}: No voxels found!")
            continue

        # Get voxel coordinates
        voxel_coords = np.argwhere(mask)

        # Convert to RAS coordinates (FreeSurfer surface space)
        ras_coords = nib.affines.apply_affine(affine, voxel_coords)

        # Convert to MNI space
        mni_coords = apply_talairach_transform(ras_coords, xfm_matrix)

        # Compute centroid
        centroid = mni_coords.mean(axis=0)

        # Volume in mm³ (each voxel is 1mm³ in FreeSurfer)
        volume_mm3 = n_voxels

        # Determine hemisphere
        hemi = 'L' if 'Left' in name else 'R'

        subcortical_data.append({
            'Region_Name': name,
            'MNI_X': centroid[0],
            'MNI_Y': centroid[1],
            'MNI_Z': centroid[2],
            'Hemisphere': hemi,
            'N_Vertices': n_voxels,
            'Area_mm2': volume_mm3,  # Using volume instead of area
            'Structure_Type': 'Subcortical'
        })

        print(f"   ✓ {name}: {n_voxels:,} voxels, centroid at ({centroid[0]:.1f}, {centroid[1]:.1f}, {centroid[2]:.1f})")

    print(f"   Extracted {len(subcortical_data)} subcortical structures ✓")
    return subcortical_data

# ==================== MAIN EXECUTION ====================

def main():
    try:
        # Check subject directory exists
        if not SUBJECT_DIR.exists():
            raise FileNotFoundError(f"Subject directory not found: {SUBJECT_DIR}")

        # Read talairach transformation
        xfm_file = SUBJECT_DIR / "mri" / "transforms" / "talairach.xfm"
        xfm_matrix = read_talairach_xfm(xfm_file)

        # Extract cortical regions
        all_regions = []

        # Left hemisphere
        lh_regions = extract_cortical_coordinates(SUBJECT_DIR, 'lh', xfm_matrix)
        all_regions.extend(lh_regions)

        # Right hemisphere
        rh_regions = extract_cortical_coordinates(SUBJECT_DIR, 'rh', xfm_matrix)
        all_regions.extend(rh_regions)

        # Extract subcortical structures
        subcortical_regions = extract_subcortical_coordinates(SUBJECT_DIR, xfm_matrix)
        all_regions.extend(subcortical_regions)

        # Create DataFrame
        df = pd.DataFrame(all_regions)

        # Sort by hemisphere and region name
        df = df.sort_values(['Structure_Type', 'Hemisphere', 'Region_Name'])

        # Save to CSV
        df.to_csv(OUTPUT_FILE, index=False, float_format='%.3f')

        print("\n" + "="*70)
        print("✅ SUCCESS!")
        print("="*70)
        print(f"Total regions extracted: {len(df)}")
        print(f"   - Cortical: {(df['Structure_Type'] == 'Cortical').sum()}")
        print(f"   - Subcortical: {(df['Structure_Type'] == 'Subcortical').sum()}")
        print(f"\n📄 Output saved to: {OUTPUT_FILE}")
        print("="*70)

        # Show sample
        print("\n📊 Sample of extracted coordinates:")
        print(df.head(10).to_string(index=False))

        return df

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    df = main()
