import pathlib


def main():
    # replace image tag in readme
    current_path = pathlib.Path(__file__)
    readme_path = current_path.parents[1] / "docs/README.rst"
    md_snippet = ':raw-html-m2r:`<img align="left" width="150" height="150" src="docs/img/airflow_helper_middle_logo.png">`'  # noqa: E501
    rst_snippet = """.. image:: img/airflow_helper_middle_logo.png
    :width: 150
    :alt: Alternative text
    """
    with open(str(readme_path), "r") as f:
        file_readme = f.read()
        content = file_readme.replace(md_snippet, rst_snippet)
        with open(str(readme_path), "w+") as f:
            f.write(content)


if __name__ == "__main__":
    main()
