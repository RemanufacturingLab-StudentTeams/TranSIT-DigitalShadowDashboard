# Digital Shadow Dashboard
The Digital Shadow Dashboard (DSD) is a tool used to visualize part location data within industrial companies. With the DSD it is possible to view: Part routes taken, Where parts concentrate or 'pile up', average time taken per location, a dynamic value stream mapping tool, viewing the differnt locations and their data, and viewing raw data in a table.

<img width="1918" height="991" alt="image" src="https://github.com/user-attachments/assets/246cb092-4796-4fe4-a919-fbd72b7d9cd9" />

# General Overview
## File structure
This project is organized into three main directories:
- code: Holds code that can be used to run the DSD locally, as well as readme for installation
- docs: Has documents about the project
- media: Has images and videos of the DSD in action

## Testing

(Automated) testing is incredibly important, both for ensuring code correctness and to formally lay down expected behaviour. The different components have different testing requirements:

### Version control
A [Git Policy](docs/policy.md) was written for this project. Please adhere to it as tightly as possible during development.

### Documentation

Documentation requirements are different depending on the subject:
- Hardware: Please include a copy of any hardware manuals within the `docs` directory. 
- Non-proprietary software: A `README.md` file suffices. This file should explain why this software is used, how to set it up locally, and how to deploy it in production.
- Proprietary software and config files: A `README.md file` is necessary, and comments should be written within the code itself explaining what it is for.
- Schemas: These should be extensively documented. A comprehensive overview of the schema should be in the `schemas` directory, with a detailed `README.md`. The idea is that a collaborator should not have to be able to understand the internal workings of a component in order to still communicate with it over a given network protocol.


# Attribution

- Project manager: [Manager of the project/project leader])
- Collaborator - "roles of the collaborator": [Name]
