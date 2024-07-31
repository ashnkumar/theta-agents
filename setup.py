from setuptools import setup, find_packages

setup(
    name='theta_agents',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'gradio', 'langgraph', 'langsmith', 'langchain', 'langchain-openai',
        'opencv-python', 'scikit-image', 'requests'  # list only necessary dependencies
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'theta-agents=theta_agents.cli:main',  # Placeholder for potential CLI
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
