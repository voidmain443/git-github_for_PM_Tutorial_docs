"""Encode real browser capture frames as one-pass GIFs and WebP stills.

Usage: python tools/encode_home_tour.py [--input tmp/home-tour-frames/capture.json]
       [--output ERP/tour-media]
Pillow is the only external dependency. No page text or data are synthesized.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, default=ROOT / 'tmp/home-tour-frames/capture.json')
    parser.add_argument('--output', type=Path, default=ROOT / 'ERP/tour-media')
    args = parser.parse_args()
    captured = json.loads(args.input.read_text(encoding='utf-8'))
    args.output.mkdir(parents=True, exist_ok=True)
    manifest = {key: captured[key] for key in ('capturedFrom', 'stage', 'viewport')}
    manifest['clips'] = []
    for clip in captured['clips']:
        raw = [Image.open(frame['file']).convert('RGB') for frame in clip['frames']]
        # A shared palette reduces distracting shifts of the navy/cream UI between states.
        contact = Image.new('RGB', (raw[0].width, raw[0].height * len(raw)))
        for i, image in enumerate(raw):
            contact.paste(image, (0, i * raw[0].height))
        palette = contact.quantize(colors=192, method=Image.Quantize.MEDIANCUT)
        gif_frames = [image.quantize(palette=palette, dither=Image.Dither.NONE) for image in raw]
        gif_path = args.output / f"{clip['id']}.gif"
        # Deliberately omit the GIF loop extension: playback ends after a single pass.
        gif_frames[0].save(gif_path, save_all=True, append_images=gif_frames[1:],
                           duration=[frame['durationMs'] for frame in clip['frames']],
                           optimize=True, disposal=2)
        frames, at_ms = [], 0
        for i, (image, source) in enumerate(zip(raw, clip['frames'])):
            filename = f"{clip['id']}-{i+1:02d}.webp"
            image.save(args.output / filename, format='WEBP', quality=86, method=6)
            frames.append({'atMs': at_ms, 'label': source['label'], 'still': filename, 'focus': source.get('focus', {'x': image.width // 2, 'y': image.height // 2})})
            at_ms += source['durationMs']
        poster = f"{clip['id']}.webp"
        # Poster is a separate stable public filename; first scene is also manually accessible.
        (args.output / poster).write_bytes((args.output / frames[0]['still']).read_bytes())
        manifest['clips'].append({
            'id': clip['id'], 'gif': gif_path.name, 'poster': poster,
            'durationMs': at_ms, 'width': raw[0].width, 'height': raw[0].height,
            'frames': frames, 'bytes': gif_path.stat().st_size,
            'sha256': hashlib.sha256(gif_path.read_bytes()).hexdigest(),
        })
    (args.output / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'clips': [{'id': clip['id'], 'durationMs': clip['durationMs'], 'bytes': clip['bytes'], 'frames': len(clip['frames'])} for clip in manifest['clips']], 'totalBytes': sum(p.stat().st_size for p in args.output.iterdir() if p.is_file())}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
