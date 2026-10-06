# Instructor guide

**Dr. Mohammed Hussin Talafha · University of Sharjah**  
*Predicting Rocket Launch Delays* · World Space Week 2026 · SSAH  
7 October 2026, 11:00–13:00 UAE time (UTC+4).

## Before participants arrive

- Open the repository's Codespaces button and check the **Python (Rocket Workshop)**
  kernel on the venue connection. Allow at least 10 minutes before the timed session.
- Ask participants to confirm GitHub/Codespaces access in advance. A laptop, browser
  and internet connection are required for Codespaces. Use pairs if access is limited.
- Run `python scripts/validate_workshop.py` after any edits. Both notebooks must work
  from fresh kernels. A full execution takes seconds to minutes, not an hour; the hour
  is for explanation, discussion, editing and interpretation.
- Keep a local Python 3.12 environment ready as a network fallback and use the saved
  notebook outputs for projection. No live dataset download or API key is needed.
- The event agenda has a broad audience. These labs assume no ML background. For
  participants unfamiliar with Python, demonstrate Shift+Enter and pair them with a
  helper; invite them to change values rather than reproduce the pipelines from memory.

## Learning goals and facilitation

Participants should leave knowing what a row, input, target and validation set are;
how future information creates misleading performance; why accuracy is not enough;
and how an alert threshold changes the trade-off between mistakes.

Repeat three ideas at the relevant activities: the data are simulated, the target
is a delay flag rather than duration, and a model estimate is not launch clearance.
Do not present the invented weather coefficients or classroom wind cut as NASA rules.

All code cells have working defaults. Ask participants to **predict, edit, run,
explain**. A success is a well-supported explanation, not the highest score.
Give one minute of quiet work before discussing each prompt. Use pairs with an
analyst at the keyboard and a reporter explaining; swap roles in hour two.

## Hour 1: 11:00–12:00

| Time | Facilitation cue | Expected evidence |
|---|---|---|
| 11:00–11:05 | Ask which of two fictional attempts is more likely to be delayed. Define T−60 and the 15-minute target. | Students can state what and when we predict. |
| 11:05–11:12 | Demonstrate kernel selection, Shift+Enter and the wind variable. | A changed number changes a Boolean. |
| 11:12–11:22 | Read the first rows. Contrast missing forecasts with missing delay on a scrub. | Students exclude actual delay and scrubbed from inputs. |
| 11:22–11:32 | Read both charts; change the wind cut and inspect sample sizes. | A sentence with a rate, a count and the word “simulated”. |
| 11:32–11:42 | Explain train / practice exam / final exam. Run the majority baseline. | Students distinguish accuracy from delay recall. |
| 11:42–11:55 | Follow one path in the tree. Try depths 1, 3 and 8. | A training–validation comparison, not just a training score. |
| 11:55–12:00 | Edit a new attempt and complete the exit ticket. | One valid input, one leaked input and one comparison. |

### Suggested answers: notebook 01

1. Changing wind from 42 to 10 changes `wind_speed > 35` from True to False.
   Explain that 35 is an invented demonstration cut.
2. `actual_delay_minutes` is unavailable at T−60 and almost directly encodes the label.
   A blank delay can indicate a scrub; it does not mean zero delay. `scrubbed` is also future information.
3. Quote the displayed rate **and count** for the chosen cut. Smaller groups give
   less stable rates. The chart describes an association in training examples.
4. Deeper trees can fit training details that do not generalise. Look for the gap;
   do not promise that every increase in depth decreases validation accuracy.
5. A changed input may leave a tree prediction unchanged because it stays in the
   same leaf. “No flag” does not guarantee punctuality.

Do not spend the entire session explaining every import. Teach the actions performed
by the pipeline: prepare training examples, learn a rule, apply it to unseen rows.

## Hour 2: 12:00–13:00

| Time | Facilitation cue | Expected evidence |
|---|---|---|
| 12:00–12:05 | Open notebook 02 with a fresh kernel. Rebuild the splits. | No dependence on notebook 01 state. |
| 12:05–12:15 | Explain numeric medians and category indicators. | Students identify the eight permitted inputs. |
| 12:15–12:25 | Compare baseline, tree and forest on identical inputs. | A validation-based choice with one remaining weakness. |
| 12:25–12:35 | Predict the effect of a lower threshold. Try missed-delay costs 1, 3 and 5. | A threshold and explicit cost assumption. |
| 12:35–12:43 | Freeze choices. Read final test counts and the confusion matrix. | Students identify a missed delay and false alarm correctly. |
| 12:43–12:55 | Compare scenarios, then change one variable. Sliders are optional. | A recorded observation; no causal or operational claim. |
| 12:55–13:00 | Complete the mini report, export and download it. | A finding, metric, trade-off and limitation. |

### Suggested answers: notebook 02

1. Wind is km/h, temperature is °C, technical items are counts. Rain and lightning
   are forecast probabilities; cloud cover is an area fraction. Pad/vehicle are categories.
   Handling a new category without crashing does not validate predictions for it.
2. Read the actual validation table; the chosen model maximises validation F1 at 0.50.
   The baseline must remain in the comparison, and a forest need not always win.
3. Lower thresholds produce more or equal flags, never fewer for fixed scores.
   Missed delays cannot increase as the threshold falls, while false alarms cannot decrease.
   The cost grid is a classroom policy. A different cost assumption can change the choice.
4. The lower-left square is delayed/scrubbed attempts predicted without a flag.
   More missed delays can mean more surprised spectators or poor resource planning.
5. Changing one input probes a fitted function, not a physical cause. Correlated
   features and unusual combinations can make the scenario unrealistic.
6. A good report states the selected model and threshold, test counts, and that all
   evidence comes from a small synthetic test set. No numerical result establishes real performance.

Use the reference outputs and `VALIDATION.md` for the default-run results. Students
who change the cost ratio can legitimately obtain a different threshold and test result.
Once they inspect test scores, discourage tuning against them; explain why a new final
assessment would require fresh data.

## Keeping to time

If behind, run the plotting and preprocessing cells as supplied, try one depth and
one cost setting, and use the plain scenario cell instead of the widget panel.
Retain the leakage discussion, baseline, final confusion matrix and exit ticket.
The optional homework is outside the 60-minute budgets. For faster groups, ask them
to explain a false alarm or find a feature change that leaves the tree prediction unchanged.

## Technical and scientific notes

- Every mission ID is unique. All training outcomes are available before the next
  split's prediction times. Real repeated attempts need grouping and time-aware evaluation.
- Missing forecasts are handled inside each pipeline. Validation/test values are
  never used to fit imputers, categories or estimators.
- The two notebooks intentionally repeat their small setup blocks. This makes
  notebook 02 runnable on its own and avoids hidden imports from workshop scripts.
- Notebook 01 uses four inputs; notebook 02 gives all its candidates the same eight.
- Both model and threshold selection reuse validation. That is deliberate in this
  beginner exercise; do not report validation performance as a final unbiased result.
- The selected model is not refit after threshold selection, so the test and scenario
  panel use the exact pipeline whose validation scores set the threshold.
- Probability calibration, real schedule snapshots, reschedules and operational drift
  are discussed as future requirements, not claimed as solved here.

## Short Arabic glossary

| English | العربية |
|---|---|
| Input / feature | مُدخل / خاصية |
| Target / label | المتغير المستهدف / التصنيف |
| Training set | بيانات التدريب |
| Validation set | بيانات التحقق لاختيار النموذج |
| Test set | بيانات الاختبار النهائي |
| Delay | تأخير |
| Scrubbed attempt | إلغاء محاولة الإطلاق |
| False alarm | إنذار كاذب |
| Missed delay | تأخير لم يتنبأ به النموذج |
| Data leakage | تسرّب المعلومات إلى النموذج |
| Decision threshold | عتبة القرار |

The notebooks use English technical explanations with Arabic title/credit lines;
use this glossary when explaining the activities bilingually.
