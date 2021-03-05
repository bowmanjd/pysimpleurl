"""Package configuration."""
import setuptools

setuptools.setup(
    author="Jonathan Bowman",
    description="Simple HTTP client that does not depend on any external libraries.",
    entry_points={"console_scripts": ["pysimpleurl=pysimpleurl:run"]},
    name="pysimpleurl",
    py_modules=["pysimpleurl"],
    version="0.1.0",
)
