"""
Base provider class for research services.
"""

from abc import ABC, abstractmethod
from typing import Tuple, Optional, List
import time
import sys


class BaseProvider(ABC):
    """Abstract base class for research providers."""

    @abstractmethod
    def create_request(
        self,
        query: str,
        model: Optional[str] = None,
        verbose: bool = False,
    ) -> Tuple[str, str]:
        """
        Create a research request.

        Args:
            query: Research question
            model: Specific model to use (optional)
            verbose: Enable verbose output

        Returns:
            Tuple of (request_id, status)
            where status is "completed" or "in_progress"
        """
        pass

    @abstractmethod
    def get_results(self, request_id: str, output_path: Optional[str] = None) -> Tuple[str, Optional[str]]:
        """
        Get research results.

        Args:
            request_id: Request ID from create_request
            output_path: Optional custom file path to save results

        Returns:
            Tuple of (markdown_report, report_file_path)
        """
        pass

    @abstractmethod
    def check_status(self, request_id: str) -> str:
        """
        Check request status.

        Args:
            request_id: Request ID from create_request

        Returns:
            Status string: "completed", "in_progress", or "failed"
        """
        pass

    def _get_adaptive_poll_interval(self, elapsed_seconds: int) -> int:
        """
        Get adaptive polling interval based on elapsed time.

        Strategy:
        - 0-10s: poll every 10s
        - 10-30s: poll every 30s
        - 30s-5min: poll every 1min
        - 5-30min: poll every 5min

        Args:
            elapsed_seconds: Total elapsed time in seconds

        Returns:
            Poll interval in seconds
        """
        if elapsed_seconds < 10:
            return 10
        elif elapsed_seconds < 30:
            return 30
        elif elapsed_seconds < 300:  # 5 minutes
            return 60
        else:  # 5+ minutes
            return 300

    def poll_until_complete(
        self,
        request_id: str,
        verbose: bool = False,
    ) -> str:
        """
        Poll request until completion with adaptive intervals.

        Polling intervals increase over time:
        - 0-10s: 10s intervals
        - 10-30s: 30s intervals
        - 30s-5min: 1min intervals
        - 5-30min: 5min intervals (max 30 minute timeout)

        Args:
            request_id: Request ID from create_request
            verbose: Enable verbose output

        Returns:
            Final status: "completed" or "failed"
        """
        start_time = time.time()
        poll_num = 0

        while True:
            elapsed = int(time.time() - start_time)
            poll_num += 1

            status = self.check_status(request_id)

            if status == "completed":
                return "completed"
            elif status == "failed":
                return "failed"

            # Calculate remaining time based on 30 min max
            max_timeout = 1800  # 30 minutes
            remaining = max(0, max_timeout - elapsed)

            if verbose:
                elapsed_mins = elapsed // 60
                remaining_mins = remaining // 60
                print(
                    f"  [Poll {poll_num}] Status: {status} "
                    f"(elapsed: {elapsed_mins}m{elapsed%60:02d}s, "
                    f"timeout: {remaining_mins}m{remaining%60:02d}s)",
                    file=sys.stderr,
                )

            # Check if we've exceeded the max timeout
            if elapsed >= max_timeout:
                print(f"  ⏱ Timeout after {elapsed}s", file=sys.stderr)
                return "in_progress"

            # Get adaptive interval and sleep
            interval = self._get_adaptive_poll_interval(elapsed)
            time.sleep(interval)

    def _get_default_model(self) -> str:
        """Get default model for this provider."""
        return "default"
