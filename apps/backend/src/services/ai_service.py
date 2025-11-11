"""
AI service for incident analysis using OpenAI.
Classifies incidents, assigns severity, and recommends actions.
"""
from typing import Dict, List, Optional
import json
from openai import OpenAI
from ..core.config import get_settings
from ..models.incident import Incident

settings = get_settings()


class AIService:
    """
    Service for AI-powered incident analysis.
    Uses OpenAI API to classify and analyze incidents.
    """
    
    def __init__(self):
        """Initialize OpenAI client."""
        # Check if we have a real API key
        if settings.openai_api_key.startswith("sk-") and len(settings.openai_api_key) > 20:
            self.client = OpenAI(api_key=settings.openai_api_key)
            self.use_mock = False
        else:
            print("⚠️  Using mock AI service (no valid OpenAI API key)")
            self.client = None
            self.use_mock = True
    
    def analyze_incident(self, incident: Incident) -> Dict[str, any]:
        """
        Analyze an incident using AI.
        
        Args:
            incident: The incident to analyze (with events loaded)
            
        Returns:
            Dictionary with:
            - category: Incident category (e.g., "database_issue")
            - severity: Priority level (P1, P2, P3)
            - summary: Human-readable summary
            - recommended_actions: List of suggested actions
        """
        if self.use_mock:
            return self._mock_analysis(incident)
        
        # Prepare context from events
        events_context = self._prepare_events_context(incident)
        
        # Create prompt for OpenAI
        prompt = self._create_analysis_prompt(incident, events_context)
        
        try:
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert DevOps engineer analyzing system incidents. "
                                   "Provide concise, actionable insights in JSON format."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            
            # Parse response
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            print(f"⚠️  OpenAI API error: {e}")
            print("Falling back to mock analysis")
            return self._mock_analysis(incident)
    
    def _prepare_events_context(self, incident: Incident) -> str:
        """
        Prepare event messages for AI analysis.
        
        Args:
            incident: Incident with events
            
        Returns:
            Formatted string of event messages
        """
        if not incident.events:
            return "No event details available"
        
        # Take up to 10 most recent events
        events = incident.events[:10]
        context_lines = []
        
        for i, event in enumerate(events, 1):
            context_lines.append(f"{i}. [{event.timestamp}] {event.message[:200]}")
        
        if len(incident.events) > 10:
            context_lines.append(f"... and {len(incident.events) - 10} more similar events")
        
        return "\n".join(context_lines)
    
    def _create_analysis_prompt(self, incident: Incident, events_context: str) -> str:
        """
        Create the prompt for OpenAI analysis.
        
        Args:
            incident: The incident
            events_context: Formatted event messages
            
        Returns:
            Prompt string
        """
        return f"""Analyze this production incident and provide a structured assessment.

**Incident Details:**
- Service: {incident.service}
- Total Events: {len(incident.events) if incident.events else 0}
- Created: {incident.created_at}

**Recent Error Messages:**
{events_context}

**Required Output (JSON):**
{{
    "category": "<one of: database_issue, memory_leak, api_timeout, authentication_error, permission_denied, network_error, configuration_error, disk_full, cpu_overload, other>",
    "severity": "<one of: P1, P2, P3>",
    "summary": "<concise 1-2 sentence description of the root cause>",
    "recommended_actions": ["<action1>", "<action2>", "<action3>"]
}}

**Severity Guidelines:**
- P1 (Critical): Service down, data loss, security breach
- P2 (High): Degraded performance, intermittent failures
- P3 (Medium): Minor issues, warnings, non-critical errors

Provide actionable, specific recommendations based on the error patterns.
"""
    
    def _mock_analysis(self, incident: Incident) -> Dict[str, any]:
        """
        Mock AI analysis when OpenAI API is not available.
        Uses simple heuristics based on error messages.
        
        Args:
            incident: The incident to analyze
            
        Returns:
            Mock analysis result
        """
        # Collect all error messages
        messages = []
        if incident.events:
            messages = [event.message.lower() for event in incident.events[:20]]
        
        combined_text = " ".join(messages)
        
        # Simple keyword-based classification
        category = "other"
        severity = "P2"
        summary = f"Multiple errors detected in {incident.service}"
        actions = ["investigate_logs", "check_service_health"]
        
        # Database issues
        if any(word in combined_text for word in ["database", "connection", "timeout", "sql", "query"]):
            category = "database_issue"
            severity = "P1"
            summary = f"Database connection issues detected in {incident.service}"
            actions = ["restart_db_service", "check_connection_pool", "verify_db_credentials"]
        
        # Memory issues
        elif any(word in combined_text for word in ["memory", "oom", "heap", "out of memory"]):
            category = "memory_leak"
            severity = "P1"
            summary = f"Memory exhaustion detected in {incident.service}"
            actions = ["restart_service", "increase_memory_limit", "analyze_heap_dump"]
        
        # API/Network issues
        elif any(word in combined_text for word in ["timeout", "503", "502", "504", "connection refused"]):
            category = "api_timeout"
            severity = "P2"
            summary = f"API timeout issues in {incident.service}"
            actions = ["check_network_connectivity", "verify_upstream_services", "scale_service"]
        
        # Authentication issues
        elif any(word in combined_text for word in ["authentication", "unauthorized", "401", "forbidden", "403"]):
            category = "authentication_error"
            severity = "P2"
            summary = f"Authentication failures in {incident.service}"
            actions = ["verify_credentials", "check_token_expiry", "review_auth_config"]
        
        # Disk issues
        elif any(word in combined_text for word in ["disk", "no space", "quota", "filesystem"]):
            category = "disk_full"
            severity = "P1"
            summary = f"Disk space issues in {incident.service}"
            actions = ["clear_old_logs", "increase_disk_quota", "archive_data"]
        
        # CPU issues
        elif any(word in combined_text for word in ["cpu", "throttle", "high load", "overload"]):
            category = "cpu_overload"
            severity = "P2"
            summary = f"High CPU usage detected in {incident.service}"
            actions = ["scale_horizontally", "optimize_queries", "review_resource_limits"]
        
        return {
            "category": category,
            "severity": severity,
            "summary": summary,
            "recommended_actions": actions
        }