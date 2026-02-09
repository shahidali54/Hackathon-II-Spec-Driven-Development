from datetime import datetime, timedelta
import calendar
from typing import Optional, Dict, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def calculate_next_occurrence(last_occurrence: datetime, recurrence_rule: Dict[str, Any]) -> Optional[datetime]:
    """
    Calculate the next occurrence date based on the recurrence rule.

    Args:
        last_occurrence: The date of the last occurrence
        recurrence_rule: Dictionary with recurrence rules

    Returns:
        datetime: The next occurrence date or None if invalid rule
    """
    if not recurrence_rule:
        return None

    frequency = recurrence_rule.get('frequency', 'daily')
    interval = recurrence_rule.get('interval', 1)

    if frequency == 'daily':
        return last_occurrence + timedelta(days=interval)
    elif frequency == 'weekly':
        return last_occurrence + timedelta(weeks=interval)
    elif frequency == 'monthly':
        # Calculate the next month considering month lengths
        target_month = last_occurrence.month + interval

        # Handle year overflow
        target_year = last_occurrence.year + (target_month - 1) // 12
        target_month = ((target_month - 1) % 12) + 1

        # Adjust for months with fewer days
        max_day = calendar.monthrange(target_year, target_month)[1]
        target_day = min(last_occurrence.day, max_day)

        try:
            return last_occurrence.replace(year=target_year, month=target_month, day=target_day)
        except ValueError:
            # If the calculated day doesn't exist (e.g., Feb 30), use the last day of the month
            return last_occurrence.replace(year=target_year, month=target_month, day=max_day)
    elif frequency == 'yearly':
        # Handle leap years - if the date doesn't exist (Feb 29 on a non-leap year), use Feb 28
        target_year = last_occurrence.year + interval
        target_month = last_occurrence.month
        target_day = last_occurrence.day

        if target_month == 2 and target_day == 29:
            # Check if the target year is a leap year
            if not calendar.isleap(target_year):
                target_day = 28

        try:
            return last_occurrence.replace(year=target_year, month=target_month, day=target_day)
        except ValueError:
            # If the calculated day doesn't exist, use the last day of the month
            max_day = calendar.monthrange(target_year, target_month)[1]
            return last_occurrence.replace(year=target_year, month=target_month, day=max_day)
    else:
        logger.error(f"Unsupported frequency: {frequency}")
        return None


def validate_recurrence_rule(recurrence_rule: Dict[str, Any]) -> bool:
    """
    Validate a recurrence rule to ensure it's properly formed.

    Args:
        recurrence_rule: Dictionary with recurrence rules

    Returns:
        bool: True if the rule is valid, False otherwise
    """
    if not isinstance(recurrence_rule, dict):
        return False

    frequency = recurrence_rule.get('frequency')
    interval = recurrence_rule.get('interval', 1)

    if not frequency or frequency not in ['daily', 'weekly', 'monthly', 'yearly']:
        logger.error(f"Invalid frequency: {frequency}")
        return False

    if not isinstance(interval, int) or interval < 1:
        logger.error(f"Invalid interval: {interval}. Must be a positive integer.")
        return False

    # Check for end condition
    end_condition = recurrence_rule.get('end_condition')
    if end_condition:
        if not isinstance(end_condition, dict):
            logger.error("End condition must be a dictionary")
            return False

        end_type = end_condition.get('type')
        if end_type not in ['after_count', 'on_date', 'never']:
            logger.error(f"Invalid end condition type: {end_type}")
            return False

    return True


def create_recurrence_rule(frequency: str, interval: int = 1, end_condition: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Create a recurrence rule with validation.

    Args:
        frequency: One of 'daily', 'weekly', 'monthly', 'yearly'
        interval: Positive integer indicating the interval between occurrences
        end_condition: Optional dictionary with end conditions

    Returns:
        dict: The validated recurrence rule
    """
    rule = {
        'frequency': frequency,
        'interval': interval,
        'enabled': True
    }

    if end_condition:
        rule['end_condition'] = end_condition
    else:
        # Default to no end condition
        rule['end_condition'] = {'type': 'never'}

    if validate_recurrence_rule(rule):
        return rule
    else:
        raise ValueError("Invalid recurrence rule")


def is_recurrence_complete(recurrence_rule: Dict[str, Any], occurrence_count: int, current_date: datetime) -> bool:
    """
    Check if a recurring task is complete based on its end condition.

    Args:
        recurrence_rule: The recurrence rule
        occurrence_count: Number of occurrences so far
        current_date: Current date for checking date-based end conditions

    Returns:
        bool: True if the recurrence is complete, False otherwise
    """
    end_condition = recurrence_rule.get('end_condition', {'type': 'never'})
    end_type = end_condition.get('type', 'never')

    if end_type == 'never':
        return False
    elif end_type == 'after_count':
        count = end_condition.get('value', 0)
        return occurrence_count >= count
    elif end_type == 'on_date':
        end_date_str = end_condition.get('value')
        if end_date_str:
            try:
                end_date = datetime.fromisoformat(end_date_str.replace('Z', '+00:00'))
                return current_date.date() >= end_date.date()
            except ValueError:
                logger.error(f"Invalid date format in end condition: {end_date_str}")
                return False

    return False