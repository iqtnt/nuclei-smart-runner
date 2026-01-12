# nuclei-smart-runner

A smart and resume-safe Nuclei automation tool designed for Bug Bounty hunters.

## ✨ Features
- Scan targets **one by one**
- Auto-remove scanned targets (resume-safe)
- Preserve Nuclei banner and live stats
- Block specific warning line:
  - `unsigned templates for scan. Use with caution`
- Append results safely (no overwrite)
- Send findings to Telegram via `notify`
- Send completion notification after all targets are scanned

## 🛠 Requirements
- Python 3.8+
- nuclei
- notify

## 🌍 Install 
```bash
git clone https://github.com/iqtnt/nuclei-smart-runner.git
cd nuclei-smart-runner
```

## 🚀 Usage

```bash
python nsr.py.py -l domains.txt -server xxxx.oast.online
```
