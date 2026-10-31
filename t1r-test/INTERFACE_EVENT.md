# Interface events around the T1-R probe

1. The paper-reader view (文献阅读 → paper → 阅读助手) did not expose a new-conversation action in the menus we inspected, so the probe used a new desktop task (新任务) with the same PDF attached.
2. First attempt: after multi-line text entry, an answer appeared before the planned explicit 发送 click, and the visible user-message export was truncated, so delivery of the appended T1-R rule was not established. It is **not counted** as a T1-R test. Its excerpt was shipped in v1.2; v1.3 drops it as an interface-fault record that supports no conclusion (the original remains in the local execution record).
3. A fresh task was opened. Its attachment picker did not respond to automation (noWindowsAvailable); the same PDF was then attached by keyboard. The rule was entered as one line, the complete pre-send field was captured (before-send-excerpt.txt), and the task completed with a 2m 10s badge. This is the valid probe.

The new-task route differs from the original reader session (it ran pdftotext itself instead of reading the reader's parsed block file); no matched comparison is claimed. The screenshot was taken after opening the PDF workbench; that viewing action does not change how the task ran.
