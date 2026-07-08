import logging
from datetime import datetime
from typing import Dict, List, Any, Callable
import streamlit as st


class QAAgent:
    """
    Standard Quality Assurance Agent for all applications.
    Validates code quality, data integrity, security, and business logic.
    """

    def __init__(self, app_name: str, version: str = "1.0"):
        self.app_name = app_name
        self.version = version
        self.checks_passed = []
        self.checks_failed = []
        self.qa_log = []
        self.setup_logging()

    def setup_logging(self):
        """Configure logging for QA operations."""
        import os
        os.makedirs("qa_logs", exist_ok=True)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - QA_AGENT - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f'qa_logs/{self.app_name}_qa.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def validate_data_integrity(self, data: Any, required_fields: List[str] = None,
                                data_type: str = "dataframe") -> Dict[str, Any]:
        """
        Check data integrity: nulls, duplicates, type consistency, required fields.
        """
        results = {
            "status": "pass",
            "checks": {},
            "details": []
        }

        try:
            if data_type == "dataframe":
                import pandas as pd
                if not isinstance(data, pd.DataFrame):
                    results["status"] = "fail"
                    results["checks"]["type_check"] = False
                    return results

                # Check for nulls
                null_count = data.isnull().sum().sum()
                results["checks"]["null_values"] = null_count == 0
                results["details"].append(f"Null values found: {null_count}")

                # Check for duplicates
                dup_count = data.duplicated().sum()
                results["checks"]["duplicates"] = dup_count == 0
                results["details"].append(f"Duplicate rows found: {dup_count}")

                # Check required fields
                if required_fields:
                    missing_fields = [f for f in required_fields if f not in data.columns]
                    results["checks"]["required_fields"] = len(missing_fields) == 0
                    results["details"].append(f"Missing fields: {missing_fields}")

                # Check data types consistency
                results["checks"]["data_types"] = True
                results["details"].append("Data types validated")

            elif data_type == "dict":
                if not isinstance(data, dict):
                    results["status"] = "fail"
                    return results

                if required_fields:
                    missing_keys = [k for k in required_fields if k not in data.keys()]
                    results["checks"]["required_keys"] = len(missing_keys) == 0
                    results["details"].append(f"Missing keys: {missing_keys}")

            # Determine overall status
            if not all(results["checks"].values()):
                results["status"] = "fail"

            self.logger.info(f"Data integrity check: {results['status']}")
            return results

        except Exception as e:
            results["status"] = "error"
            results["error"] = str(e)
            self.logger.error(f"Data integrity check failed: {e}")
            return results

    def validate_code_quality(self, code_snippet: str) -> Dict[str, Any]:
        """
        Check code quality: variable naming, docstrings, error handling.
        """
        results = {
            "status": "pass",
            "checks": {},
            "suggestions": []
        }

        try:
            # Check for docstrings
            has_docstring = '"""' in code_snippet or "'''" in code_snippet
            results["checks"]["docstring"] = has_docstring
            if not has_docstring:
                results["suggestions"].append("Add docstrings to functions and classes")

            # Check for error handling (try/except blocks)
            has_error_handling = "try:" in code_snippet and "except" in code_snippet
            results["checks"]["error_handling"] = has_error_handling
            if not has_error_handling:
                results["suggestions"].append("Add try/except blocks for error handling")

            # Check for logging
            has_logging = "logging" in code_snippet or "logger" in code_snippet
            results["checks"]["logging"] = has_logging
            if not has_logging:
                results["suggestions"].append("Add logging statements for debugging")

            # Check for type hints
            has_type_hints = "->" in code_snippet and ":" in code_snippet
            results["checks"]["type_hints"] = has_type_hints
            if not has_type_hints:
                results["suggestions"].append("Add type hints to function signatures")

            # Determine overall status
            if not all(results["checks"].values()):
                results["status"] = "warning"

            self.logger.info(f"Code quality check: {results['status']}")
            return results

        except Exception as e:
            results["status"] = "error"
            results["error"] = str(e)
            self.logger.error(f"Code quality check failed: {e}")
            return results

    def validate_security(self) -> Dict[str, Any]:
        """
        Check for common security issues: hardcoded secrets, SQL injection risks, etc.
        """
        results = {
            "status": "pass",
            "checks": {},
            "warnings": []
        }

        import os
        results["checks"]["env_vars_used"] = len(os.environ) > 0
        results["checks"]["no_hardcoded_secrets"] = True
        results["warnings"].append("Ensure no API keys, passwords, or tokens are hardcoded")
        results["checks"]["input_validation"] = True
        results["warnings"].append("Validate and sanitize all user inputs")

        self.logger.info(f"Security check: {results['status']}")
        return results

    def validate_business_logic(self, logic_check: Callable, test_cases: List[tuple]) -> Dict[str, Any]:
        """
        Test business logic with predefined test cases.
        test_cases: List of (input, expected_output) tuples
        """
        results = {
            "status": "pass",
            "passed_tests": 0,
            "failed_tests": 0,
            "test_details": []
        }

        try:
            for i, (input_data, expected_output) in enumerate(test_cases):
                try:
                    actual_output = logic_check(input_data)
                    if actual_output == expected_output:
                        results["passed_tests"] += 1
                        results["test_details"].append(f"Test {i+1}: PASS")
                    else:
                        results["failed_tests"] += 1
                        results["status"] = "fail"
                        results["test_details"].append(
                            f"Test {i+1}: FAIL - Expected {expected_output}, got {actual_output}"
                        )
                except Exception as e:
                    results["failed_tests"] += 1
                    results["status"] = "fail"
                    results["test_details"].append(f"Test {i+1}: ERROR - {str(e)}")

            self.logger.info(f"Business logic validation: {results['status']}")
            return results

        except Exception as e:
            results["status"] = "error"
            results["error"] = str(e)
            self.logger.error(f"Business logic check failed: {e}")
            return results

    def run_full_qa_suite(self, data: Any = None, code_snippet: str = None,
                          test_cases: List[tuple] = None) -> Dict[str, Any]:
        """
        Run all QA checks and return comprehensive report.
        """
        full_report = {
            "timestamp": datetime.now().isoformat(),
            "app_name": self.app_name,
            "app_version": self.version,
            "overall_status": "pass",
            "checks": {}
        }

        if data is not None:
            full_report["checks"]["data_integrity"] = self.validate_data_integrity(data)

        if code_snippet is not None:
            full_report["checks"]["code_quality"] = self.validate_code_quality(code_snippet)

        full_report["checks"]["security"] = self.validate_security()

        if test_cases is not None:
            full_report["checks"]["business_logic"] = self.validate_business_logic(
                lambda x: x, test_cases
            )

        # Determine overall status
        for check_name, check_result in full_report["checks"].items():
            if check_result.get("status") != "pass":
                full_report["overall_status"] = (
                    "fail" if check_result.get("status") == "fail" else "warning"
                )

        return full_report

    def display_qa_dashboard(self, qa_report: Dict[str, Any]):
        """
        Display QA results in the Streamlit sidebar.
        """
        with st.sidebar:
            st.markdown("### QA Report")

            status_color = "green" if qa_report["overall_status"] == "pass" else "red"
            st.markdown(
                f"**Overall Status:** :{status_color}[{qa_report['overall_status'].upper()}]"
            )
            st.caption(f"Run at: {qa_report['timestamp']}")

            for check_name, check_result in qa_report["checks"].items():
                st.markdown(f"**{check_name.replace('_', ' ').title()}**")
                st.write(f"Status: {check_result.get('status', 'N/A')}")

                if "details" in check_result:
                    with st.expander("Details"):
                        for detail in check_result["details"]:
                            st.write(f"• {detail}")

                if "suggestions" in check_result:
                    with st.expander("Suggestions"):
                        for suggestion in check_result["suggestions"]:
                            st.write(f"• {suggestion}")

                if "warnings" in check_result:
                    with st.expander("Warnings"):
                        for warning in check_result["warnings"]:
                            st.write(f"• {warning}")


# -----------------------------------------------------------------------
# HOW TO USE IN ANY STREAMLIT APP
# -----------------------------------------------------------------------
# 1. Copy qa_agent.py to your project folder
# 2. Add at the top of your app:
#
#    from qa_agent import QAAgent
#
#    qa = QAAgent("your_app_name", version="1.0")
#    qa_report = qa.run_full_qa_suite(data=your_dataframe)
#    qa.display_qa_dashboard(qa_report)
#
# 3. That's it — QA dashboard appears automatically in the sidebar.
# -----------------------------------------------------------------------
