# Hive

# Description

Hive is an innovative platform designed to tackle the complexities of collective problem-solving through a structured,
evidence-based approach to decision-making. By leveraging the power of collaborative sensemaking, Hive enables
communities, teams, and institutions to navigate intricate challenges more effectively. Hive is built on a foundation of
collective intelligence, enabling users to harness the wisdom of the crowd to make better decisions, solve complex
problems, and drive innovation.

Read the [wiki](https://github.com/Voidcake/Hive/wiki) for more context.

# Table of Contents

1. Installation
2. Usage
3. Features
4. Contributing
5. License
6. Contact

# Installation

Clone the repository:
git clone https://github.com/Voidcake/Hive

Navigate to the project directory:
`cd yourproject`

Create a virtual environment:
`python -m venv venv`

Activate the virtual environment:
On macOS and Linux:
`source venv/bin/activate`
On Windows:
`.\venv\Scripts\activate`

Install the required packages:
`pip install -r requirements.txt`

# Usage

1. Create and run a local Neo4j database instance (version >= 5.0.0) or use
   a [hosted Neo4j instance](https://neo4j.com/cloud/platform/aura-graph-database/).
2. Setup environment variables for the database connection details using the .env.example file as a template.
3. Update the database connection details in the `config.py` file.
4. Run the main script in dev mode: `<path_to_venv> -m uvicorn core.main:app --reload`
5. Open a web browser and navigate to http://127.0.0.1:8000/graphql to access the GraphQL playground to explore the Docs
   and
   interact with the API.

# Features

_Note: This project is currently in its early prototyping stage. The present prototype is a self-hosted GraphQL API
focused
on basic collective sensemaking functionalities, with advanced data pipelines, rich UI and decision-making capabilities
planned for future iterations._

The current prototype features the following:

- User authentication
- CRUD operations for Users, Townsquares, Questions, Claims, Premises, and Evidence
- Complex queries and mutations for creating and managing complex argumentation structures via a GQL API

Planned features include:

- Basic Argument Mining capabilities for extracting argumentation structures from unstructured text
- Graph Analytics for identifying key nodes and relationships in argumentation structures
- Semantic search capabilities for finding relevant content
- Similarity-based recommendation system for suggesting related content
- Integration with external data sources for importing data
- Advanced data visualization capabilities for exploring argumentation structures
- Decision-support tools for facilitating group decision-making
- RDF export capabilities for interoperability with other systems

# Contributing

Fork the repository.

Create a new branch:
`git checkout -b feature/YourFeature`

Make your changes and commit them:
`git commit -m "Add YourFeature"`

Push to the branch:
`git push origin feature/YourFeature`

Open a pull request.

# License

This project is licensed under the MIT License. See the LICENSE file for more details.

# Wiki

For more information, please refer to the [wiki](https://github.com/Voidcake/Hive/wiki)!

# Contact

Feel free to reach out to the project maintainers with any questions or feedback:

Anthony Aflatoun - anthony_pierre.aflatoun@smail.th-koeln.de  
Project Link: https://github.com/Voidcake/Hive