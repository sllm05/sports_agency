"""
Modular Multi-Agent Architecture for Sports Agency Strategy Desk (`src/sports_agency/agents/__init__.py`)

Exposes specialized, independent agent modules:
- BaseAgent: Core agent interface and MCP tool calling protocol
- SupervisorAgent: Workflow routing and track orchestration (Node 1)
- ScoutingAnalystAgent: Hermes scouting, club matching and valuation (Node 2A)
- RenewalAnalystAgent: Contract renewal and replacement amortization savings (Node 2B)
- CareerStrategistAgent: Career timing and 3-year growth roadmap (Node 2C)
- LegalComplianceAgent: SQLite Vector RAG and GBE work permit scoring (Node 3)
- NegotiationSparringAgent: Adversarial negotiation sparring simulator & HITL (Node 4A, 4B)
- DocumentWriterAgent: Triple-output practical markdown deliverables (Node 5)
"""

from sports_agency.agents.base import (
    BaseAgent,
    apply_contract_override,
    invoke_hermes_mcp_tool,
)
from sports_agency.agents.career_strategist import CareerStrategistAgent
from sports_agency.agents.document_writer import DocumentWriterAgent
from sports_agency.agents.legal_compliance import LegalComplianceAgent
from sports_agency.agents.negotiation_sparring import NegotiationSparringAgent
from sports_agency.agents.renewal_analyst import RenewalAnalystAgent
from sports_agency.agents.scouting_analyst import ScoutingAnalystAgent
from sports_agency.agents.supervisor import SupervisorAgent

# Default singleton instances for standard workflow orchestration
SUPERVISOR_AGENT = SupervisorAgent()
SCOUTING_ANALYST_AGENT = ScoutingAnalystAgent()
RENEWAL_ANALYST_AGENT = RenewalAnalystAgent()
CAREER_STRATEGIST_AGENT = CareerStrategistAgent()
LEGAL_COMPLIANCE_AGENT = LegalComplianceAgent()
NEGOTIATION_SPARRING_AGENT = NegotiationSparringAgent()
DOCUMENT_WRITER_AGENT = DocumentWriterAgent()

__all__ = [
    # Base utilities
    "BaseAgent",
    "apply_contract_override",
    "invoke_hermes_mcp_tool",
    # Agent Classes
    "SupervisorAgent",
    "ScoutingAnalystAgent",
    "RenewalAnalystAgent",
    "CareerStrategistAgent",
    "LegalComplianceAgent",
    "NegotiationSparringAgent",
    "DocumentWriterAgent",
    # Singleton Agent Instances
    "SUPERVISOR_AGENT",
    "SCOUTING_ANALYST_AGENT",
    "RENEWAL_ANALYST_AGENT",
    "CAREER_STRATEGIST_AGENT",
    "LEGAL_COMPLIANCE_AGENT",
    "NEGOTIATION_SPARRING_AGENT",
    "DOCUMENT_WRITER_AGENT",
]
