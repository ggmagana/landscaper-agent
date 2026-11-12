.PHONY: test run evals check
test:
	python3 -m pytest -q
evals:
	python3 evals/run_evals.py
check:
	python3 scripts/check_deploy.py
run:
	uvicorn landscaper.main:app --reload --port 8000
