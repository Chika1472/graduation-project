"""Select performance-detail candidates; distance uses the supplied boundary snapshot.

Requires pyshp, pyproj and shapely. Uses local cached packages when present.
Name matching is only a download filter. Final joins must use detail API IDs.
"""
from pathlib import Path
import collections
import sys
import unicodedata

cache = Path.home() / '.cache/grad-python'
if cache.exists():
    sys.path.insert(0, str(cache))
import shapefile
import shapely
from shapely.geometry import Point, shape
from pyproj import CRS, Transformer
import download_kopis as k


def norm(value):
    return ''.join(unicodedata.normalize('NFKC', value).replace('(폐관)', '').split())


def main():
    directory = k.ROOT / 'data/raw/seoul_areas/extracted'
    shp = next(directory.glob('*.shp'))
    crs = CRS.from_wkt(shp.with_suffix('.prj').read_text())
    transformer = Transformer.from_crs('EPSG:4326', crs, always_xy=True)
    reader = shapefile.Reader(str(shp), encoding=shp.with_suffix('.cpg').read_text().strip())
    areas = []
    repairs = []
    for record in reader.iterShapeRecords():
        values = record.record.as_dict()
        if str(values['SIGNGU_CD']) not in ('11110', '11440'):
            continue
        geom = shape(record.shape.__geo_interface__)
        if not geom.is_valid:
            reason = shapely.is_valid_reason(geom)
            geom = shapely.make_valid(geom)
            if geom.geom_type == 'GeometryCollection':
                geom = shapely.union_all([g for g in geom.geoms
                                          if g.geom_type in ('Polygon', 'MultiPolygon')])
            if geom.is_empty or not geom.is_valid:
                raise ValueError(f'Unrepairable area geometry {values["TRDAR_CD"]}')
            repairs.append({'area_id': str(values['TRDAR_CD']), 'reason': reason,
                            'method': 'shapely.make_valid, polygon parts only'})
        areas.append((str(values['TRDAR_CD']), str(values['SIGNGU_CD']), geom))
    if not areas:
        raise ValueError('No target district polygons')
    facility_list = k.read_csv('facilities_list_seoul.csv')
    facilities = k.read_csv('facilities_detail_seoul.csv')
    nearby = set()
    links = []
    valid = set()
    invalid = []
    for row in facilities:
        try:
            lon, lat = float(row['lo']), float(row['la'])
            if not (124 <= lon <= 132 and 33 <= lat <= 39):
                raise ValueError('Coordinates outside Korea')
            point = Point(*transformer.transform(lon, lat))
            valid.add(row['mt10id'])
        except (ValueError, KeyError):
            invalid.append(row['mt10id'])
            continue
        for area_id, district_id, poly in areas:
            distance = point.distance(poly)
            if distance <= 800:
                nearby.add(row['mt10id'])
                links.append({'mt10id': row['mt10id'], 'area_id': area_id,
                              'district_code': district_id, 'distance_m': round(distance, 3),
                              'within_300m': int(distance <= 300),
                              'within_500m': int(distance <= 500), 'within_800m': 1})
    k.write_csv('venue_area_links_800m.csv', links)
    names = collections.defaultdict(list)
    for row in facility_list:
        names[norm(row['fcltynm'])].append(row)
    candidates = []
    excluded = []
    for row in k.read_csv('performances_list_seoul_2023_2025.csv'):
        name = norm(row['fcltynm'])
        matches = names.get(name, [])
        if not matches:
            prefixes = [n for n in names if name.startswith(n + '(')]
            if prefixes:
                matches = names[max(prefixes, key=len)]
        reasons = []
        if not matches:
            reasons.append('unmatched_facility_name')
        if any(f['mt10id'] not in valid for f in matches):
            reasons.append('facility_coordinate_unavailable')
        if any(f['gugunnm'] in ('종로구', '마포구') for f in matches):
            reasons.append('target_district')
        if any(f['mt10id'] in nearby for f in matches):
            reasons.append('within_800m_of_target_area')
        if len(matches) > 1:
            reasons.append('ambiguous_facility_name')
        record = dict(row, candidate_reason=';'.join(reasons),
                      candidate_mt10ids=';'.join(sorted(f['mt10id'] for f in matches)))
        (candidates if reasons else excluded).append(record)
    k.write_csv('performance_detail_candidates.csv', candidates)
    k.write_csv('performance_detail_excluded_by_location.csv', excluded)
    report = {
        'target_area_polygons': len(areas), 'facility_coordinate_rows': len(valid),
        'invalid_coordinate_facilities': invalid,
        'facilities_missing_details': sorted({r['mt10id'] for r in facility_list} -
                                             {r['mt10id'] for r in facilities}),
        'nearby_facilities_800m': len(nearby), 'venue_area_relations': len(links),
        'performance_detail_candidates': len(candidates), 'excluded_performances': len(excluded),
        'coordinate_assumption': 'KOPIS longitude/latitude interpreted as EPSG:4326',
        'projected_crs': crs.to_string(), 'boundary_snapshot': str(shp.relative_to(k.ROOT)),
        'derived_geometry_repairs': repairs,
        'note': 'Current facility coordinates and boundary snapshot; historical moves/boundaries unverified. Facility names only shortlist downloads; actual detail IDs are used for final joins.',
    }
    k.save_json(k.ROOT / 'metadata/kopis_spatial_inventory.json', report)
    print({key: report[key] for key in ['target_area_polygons', 'facility_coordinate_rows',
          'nearby_facilities_800m', 'venue_area_relations', 'performance_detail_candidates',
          'excluded_performances']})
    print('Geometry repairs:', len(repairs))


if __name__ == '__main__':
    main()
