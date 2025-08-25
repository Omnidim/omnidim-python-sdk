from setuptools import setup, find_packages

setup(
    name="omnidimension",
    version="0.2.11",
    packages=find_packages() + ["omnidim_mcp_server"],
    install_requires=["requests"],
    extras_require={
        "mcp": ["fastapi>=0.95.0", "uvicorn>=0.21.0", "fastmcp>=0.1.0", "pydantic>=1.10.0"]
    },
    entry_points={
        "console_scripts": [
            "omnidim-mcp-server=omnidim_mcp_server.main:create_app",
        ],
    },
    author="https://www.omnidim.io/",
    author_email="kevin@omnidim.io",
    description="SDK and MCP Server for Omni Assistant services",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/kevin-omnidim/omnidim-sdk",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)