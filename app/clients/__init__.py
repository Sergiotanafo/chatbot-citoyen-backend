"""
app/clients/__init__.py
Clients de communication avec les services externes et le DSP.
"""

from app.clients.dsp_client import DspClient, dsp_client

__all__ = ["DspClient", "dsp_client"]

