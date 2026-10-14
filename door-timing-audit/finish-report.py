from pathlib import Path
import json
root=Path.cwd();audit=root/'door-timing-audit';final=json.loads((audit/'browser-sequences-final.json').read_text());edges=json.loads((audit/'edge-checks.json').read_text());scope=json.loads((audit/'scope-verification.json').read_text());baseline=json.loads((audit/'browser-sequences.json').read_text())
assert all(r['pass'] for r in edges)
checks=[]
for r in final:
 normal=r['mode']!='reduced-motion';closed=max(s['media'] for s in r['samples'] if not s['finished']);transforms={s['transform'] for s in r['samples'] if s['opening'] and not s['finished']};
 passes=not r['errors'] and r['video']['rate']==1 and not r['video']['paused'] and closed<=.05 and (not normal or (r['frames'][0]['media']<=.05 and len(transforms)>8))
 assert passes
 checks.append({'width':r['width'],'mode':r['mode'],'pass':passes,'media_at_reveal':r['frames'][0]['media'],'max_media_behind_doors':closed,'sampled_door_transforms':len(transforms),'playback_rate':r['video']['rate'],'dropped_video_frames':r['quality']['dropped']})
(audit/'verification-summary.json').write_text(json.dumps({'fresh_load_scenarios':checks,'fallback_checks':edges,'scope':scope},indent=2),encoding='utf-8')
text='''DOMMYDOM HOMEPAGE DOOR / VIDEO TIMING
October 14, 2026. Local changes only; no commit, push, or publication.

Finding
The original footage and both delivered clips begin with Dominique smiling toward the camera. The camera-facing portion is approximately the first half-second; she starts turning within the first second. Continuous-playback frame inspection confirmed the same opening in the original 1920x1080 file and the existing 1280x720 desktop / 640x360 mobile files.
The existing door CSS runs for 1.05 seconds after a 0.1-second animation delay. Previously the HTML started native autoplay independently of the controller, and the controller also requested playback before the doors finished. Fresh baseline tests found the video already at about 1.44 seconds on desktop and 1.23 seconds on mobile at the full reveal, after Dominique had begun turning away.

Correction
Removed native HTML autoplay so loading/parsing cannot consume the opening shot behind the doors. The existing controller now prepares the decoded first frame and holds video time at zero throughout the unchanged door animation. It uses the actual right-door animationend event to finish the reveal, retaining the existing 1.25-second fallback timer if that event is unavailable.
After the doors finish, a 450 ms opening beat precedes normal playback. That brief beat plus the natural camera-facing opening footage gives approximately one second facing the camera after the full reveal. Playback then continues uninterrupted at its original 1x rate. No mid-movement pause, reverse playback, slowed frames, re-encoding, or new loading screen was introduced. The rest of the page remains visible and interactive independently of the video.
The existing user-gesture Play video fallback, Open video error fallback, looping, and reduced-motion behavior are preserved. Failed-source handling covers errors on source elements and failures occurring before the deferred controller attaches, preventing an unavailable clip from leaving the doors closed. Reduced-motion viewers retain the immediate reveal without the opening beat.

Files changed for this adjustment
index.html: removed the introduction video's autoplay attribute; updated only its controller cache version to 20261014-door-sync.
assets/home-playback-v23.js: synchronized the first-frame preparation, unchanged door animation, short reveal beat, and playback/fallback lifecycle.
No door CSS, page layout, navigation, other animations, or video file was changed. Before/after hashes confirm every other checked website asset and root HTML page remains unchanged. Exact homepage comparison confirms its only markup changes are the two video/controller changes above. Prior performance-task edits remain untouched.

Testing
Fresh browser contexts tested desktop 1440x1000 and mobile emulation 390x844, including the mobile video source and touch behavior. Baseline and corrected sequences were captured from initial navigation, with playback events, door animation events/transforms, wall time, media time, and decoded video frames.
All six final fresh-load scenarios passed: desktop/mobile normal loads, desktop/mobile media responses delayed three seconds, and desktop/mobile reduced motion. Normal and delayed-media runs kept video time at 0.00 throughout the doors and at full reveal. Sampled frames around 0.9 seconds after reveal show Dominique still facing the camera; subsequent frames show her natural turn and walk. Playback rate remains 1. All tested final sequences recorded zero dropped video frames and zero JavaScript errors. Door transform samples confirm the existing animation continued through multiple positions rather than snapping open.
Ten additional desktop/mobile checks passed: camera-facing full-hero screenshot, playback rejected until a real click, suppressed animationend event fallback, failed media requests, and continuing through a complete video loop. Testing found and corrected a failed-download readiness edge case before completion.
Video and stylesheet hashes are unchanged. Git diff whitespace validation passes. No artificial page-loading delay or visibility gate was added; only the introduction video's progression is coordinated with the doors.

Evidence / review
reveal-facing-1440.png and reveal-facing-390.png show the actual desktop/mobile hero at the full reveal.
after-1440-normal-sequence.jpg and after-390-normal-sequence.jpg show the decoded clip at reveal, +250ms, +500ms, +900ms, +1100ms, +1600ms, and +2400ms.
browser-sequences.json preserves baseline evidence. browser-sequences-final.json contains the final full sequence measurements. edge-checks.json, verification-summary.json, and scope-verification.json record the checks above. Source/video inspection montages and local test scripts are retained in this folder. The screenshots/montages are review evidence, not replacement website media.

Limits
These are local headless Chrome tests with mobile viewport/touch emulation, not physical iPhone/Android or Safari/Firefox tests. External scripts/fonts were blocked to isolate the homepage sequence. No live deployment, analytics, or backend submission testing was performed. Video timing is synchronized to decoded readiness and the actual door event rather than assumed network load time, and delayed-media cases were tested. Temporary test packages are removed after testing.
'''
(audit/'REPORT.txt').write_text(text,encoding='utf-8');print(json.dumps(checks,indent=2))
