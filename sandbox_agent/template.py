from e2b import Template, default_build_logger

from sandbox_agent.config import SANDBOX_PACKAGES, SANDBOX_TEMPLATE_NAME


def build_template() -> None:
    template = (
        Template()
        .from_template("code-interpreter-v1")
        .pip_install(SANDBOX_PACKAGES)
    )
    Template.build(
        template,
        SANDBOX_TEMPLATE_NAME,
        on_build_logs=default_build_logger(),
    )


def ensure_template() -> None:
    if not Template.exists(SANDBOX_TEMPLATE_NAME):
        build_template()
