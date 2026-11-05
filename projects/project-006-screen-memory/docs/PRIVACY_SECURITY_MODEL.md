# P009 privacy and security model

Required by the project boundary before any continuous capture is implemented. The code must match this document; tests check the rules marked **[tested]**.

## 1. Who and what it protects
The only intended user is the person at the computer, recording their own screen for their own later use. It must not become a way to watch someone else.

| Asset | Risk |
|---|---|
| Screen images | Passwords, messages, bank details, other people's information, anything on screen |
| Window titles | Reveal documents, sites, people and searches |
| Usage timeline | Shows when and how the person works |

| Threat | Response |
|---|---|
| Someone copies the data folder (another account, a backup, a stolen disk) | Images encrypted with Windows DPAPI, tied to the user's Windows account **[tested with a fake protector]** |
| A web page or another local program calls the local API | Bound to 127.0.0.1 only; every request needs a per-run secret token; `Host` header must be local (blocks DNS rebinding) **[tested]** |
| Capturing something the user would not want kept | Default exclusions, pause, delete recent, retention limit, storage cap (below) |
| Recording someone else covertly | Not a design goal. Capture only starts when the user starts it in a visible console; the dashboard always shows the state; there is no hidden or remote mode. |

Not protected against: malware running as the same Windows user (it can read anything the user can), and anyone who knows the user's Windows password. Window titles and recognised text are stored unencrypted in the local database so they can be searched; the database sits in the user's own profile folder.

## 2. Capture rules
1. **Off until started.** Nothing is recorded until the user runs `python -m p009 record` and confirms. Stopping the program stops capture.
2. **Pause and resume** from the dashboard; while paused nothing is captured or buffered **[tested]**.
3. **Only the foreground window**, not the whole screen, so other windows and other people's content on the screen are not taken.
4. **Exclusions checked before an image is taken** **[tested]**:
   - programs: password managers (KeePass, KeePassXC, 1Password, Bitwarden, LastPass, Dashlane), Windows Credential UI, Windows Security;
   - window titles containing: InPrivate, Incognito, Private Browsing, password, sign in, log in, login, bank, banking, PayPal, credit card;
   - anything the user adds.
   An excluded window leaves no image and no title, only a count of skipped checks.
5. **Selective capture (policy B4)** keeps an image only when something meaningful changed, so far fewer images are kept than with fixed-interval capture (section 5).
6. **Screen locked or user idle:** nothing is captured.

## 3. Retention and control
| Control | Default |
|---|---|
| Retention | 7 days; older items are deleted at start-up and every hour **[tested]** |
| Storage cap | 2 GB; oldest items deleted first when exceeded **[tested]** |
| Delete the last 15 minutes / last hour | Dashboard buttons **[tested]** |
| Delete one item | Dashboard |
| Delete everything | Dashboard, with confirmation; removes the database rows and image files **[tested]** |
| Export | Not provided in this version, so data does not leave the device by accident |

Deleted image files are removed from disk; the encrypted files are not securely wiped (SSD wear-levelling makes that unreliable anyway).

## 4. Processing
Everything stays on the computer: no network calls, no cloud OCR or AI. Text recognition, when used, is the offline Windows OCR engine.

## 5. Capture policies (for the research evaluation)
All policies see the same stream of observations and none sees task labels or the future.

| Policy | Keeps an image when |
|---|---|
| B0 dense | every 2 s |
| B1 sparse | every 30 s |
| B2 visual change | the window image changed by more than 8 % since the last kept image |
| B3 event-triggered | window or title change, a typing pause of 2 s, or 60 s without a capture |
| B4 selective | as B3, but skips images nearly identical to the last kept one from the same window, never keeps excluded windows, and when you leave a window it keeps that window's last frame (the "where was I" frame) |

B0–B3 also skip excluded windows in the live app; the offline evaluation reports what each policy *would* have retained, so the privacy cost of naive capture can be measured.

## 6. What is not done
- No study with people: the research question (task-resumption performance) needs participants and ethics approval.
- No screen-reader or accessibility API text capture.
- macOS and Linux capture are not implemented; the program refuses to record there.
