# Phoenix Checklist V4 — Agent Live Trading Rollout

## 🎯 מטרת גרסה V4
הפיכת הסוכן למערכת מסחר פעילה, מגיבה, מדווחת — עם דשבורד אינטראקטיבי, יכולת הצעת טריידים, ביצוע בפייפר-טרייד, הפקת דוחות, וניטור בזמן אמת.

כל פעולה ניתנת למעקב, מופעלת על פי לחיצת כפתור או תזמון, ומגובה בקוד, נתונים ודוחות.

---

## ✅ Foundation
- [ ] חיבור מלא בין dashboard ↔ agent
- [ ] callbacks לכל כרטיס בדשבורד
- [ ] ניהול סטייט פנימי של agent runtime
- [ ] הרחבת CLI לכל פונקציה תפעולית

## 📊 Data
- [ ] משיכת live data מתוזמנת אוטומטית (cron או stream)
- [ ] בדיקת איכות ו־anomaly בזמן אמת
- [ ] שמירה מקומית (Parquet) לפי asset/date

## 🧠 Features
- [ ] חישוב מתוזמן של פיצ'רים
- [ ] הרחבה לפיצ'רים מרובי טווחים (multi-timeframe)
- [ ] תיקוף פיצ'רים בזמן אמת על live data

## 🎯 Labeling
- [ ] ריצת labeling רציפה / יומית לפי קונפיג
- [ ] סימון טריידים עדכניים למעקב

## 🔮 Models
- [ ] טעינה מיידית של המודל המוביל (champion)
- [ ] `agent.propose()` מחזיר טריידים עם פרטי confidence + SHAP
- [ ] תמיכה ב־challenger + retrain ע"פ drift

## 🔁 Backtest
- [ ] אופטימיזציית params לפי יומן ביצועים
- [ ] שמירת תרחישים נפרדים לכל אסטרטגיה

## 🔬 Validation
- [ ] מנגנון בדיקות leakage / timing לפני כל אימון
- [ ] בדיקת ביצועים מול baseline חיצוני

## 🧯 Risk
- [ ] ניהול sizing, stops, caps אונליין
- [ ] ניתוח risk/reward לכל הצעה

## 🧾 Reports
- [ ] דוחות PDF יומיים / שבועיים לפי תבנית
- [ ] דוחות SHAP עם מפת feature impact

## 📡 Monitor
- [ ] PSI / KS יומיים
- [ ] התראות בזמן אמת (alerts.yaml)
- [ ] heartbeat.json מעודכן כל שעה

## 📜 Compliance
- [ ] רישום פעולות, הצעות וביצועים ב־`decisions/`
- [ ] סנכרון audit log לפי רגולציה (SEC/ESMA)

## 🚀 Decisions
- [ ] `propose → approve → execute → track` cycle מתוזמן או לפי לחיצה
- [ ] שימוש ב־dashboard כ־control panel פעיל
- [ ] כל לחיצה מייצרת רישום והפעלה מלאה

## 🎁 Packs
- [ ] הגדרת חבילות הפעלה (`packs/`) לפי סגנון מסחר: momentum, mean-reversion, news-driven
- [ ] תזמון pack יומי לפיילוט

---

## ✅ Output בסוף V4
- דשבורד שמציג ומפעיל את הסוכן המלא
- פעולות real-time, כולל טריידים וניתוחים
- ניטור מתמשך והצעות לשיפור
- מוכנות ל־Profitability Test תחת פייפר-טרייד

> "V3 בנה תשתית — V4 בונה Agent שמרוויח."
