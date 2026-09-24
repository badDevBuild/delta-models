"""Bind slicing claims to the current master, actual plate inputs and native output."""
from pathlib import Path
import hashlib
import json
import zipfile

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def check_slicing(asset):
    asset=Path(asset)
    directory=asset/'print'
    report_path=directory/'slice-validation.json'
    if not report_path.is_file():
        return {'passed':False,'errors':['No slicing report'],'report':{}}
    errors=[]
    try:
        report=json.loads(report_path.read_text())
        if report.get('passed') is not True:
            errors.append('Slicer did not report success')
        source=asset/'source'/(asset.name+'.blend')
        if report.get('source_sha256')!=digest(source):
            errors.append('Master changed after slicing')
        project_root=asset.parents[1].resolve()
        for profile in report.get('profiles',[]):
            profile_path=(project_root/profile['file']).resolve()
            if not profile_path.is_relative_to(project_root) or not profile_path.is_file() or digest(profile_path)!=profile['sha256']:
                errors.append('Missing or changed slicing profile: '+profile['file'])

        def checked_file(name,expected):
            path=(directory/name).resolve()
            if not path.is_relative_to(directory.resolve()):
                raise ValueError('Artifact path leaves print directory')
            if not path.is_file() or not expected or digest(path)!=expected:
                errors.append('Missing or changed artifact: '+name)
            return path

        plates=report.get('plates',[])
        expected={p['file'] for p in json.loads((directory/'plates.json').read_text())['plates']}
        covered=set()
        for plate in plates:
            checked_file(plate['input_file'],plate['input_3mf_sha256'])
            original=plate.get('original_input_file')
            if original:
                checked_file(original,plate['original_input_sha256'])
            covered.add(original or plate['input_file'])
        if covered!=expected:
            errors.append('Slicing coverage differs from current geometry plate set')
        native=report.get('native_projects',[])
        if len(native)!=len(plates) or not native:
            errors.append('Native project count differs from sliced plate count')
        for entry in native:
            path=checked_file(entry['file'],entry['sha256'])
            if path.is_file():
                with zipfile.ZipFile(path) as archive:
                    paths=archive.namelist()
                    if not any(p.endswith('.gcode') and archive.getinfo(p).file_size>0 for p in paths):
                        errors.append('Native project contains no G-code: '+entry['file'])
        return {'passed':not errors,'errors':errors,'report':report}
    except (OSError,ValueError,KeyError,TypeError,zipfile.BadZipFile) as exc:
        return {'passed':False,'errors':errors+[str(exc)],'report':{}}
