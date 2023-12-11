# Capstone Project


Tellatale is not just a journal; it's your dynamic companion for crafting captivating entries with the added magic of AI and ChatGPT. Functioning as a chatbot within the innovative LangChain framework, Tellatale goes beyond traditional journaling.

Upon initiation, the application seamlessly guides users through a user-friendly three-step process. Initially, the chat engages users by requesting their name. If the user is already in the system, additional information is seamlessly incorporated, allowing the chatbot to maintain an ongoing and personalized interaction.

The application's intelligence doesn't stop there. It checks the user's status to tailor the experience further. For users who have not yet been profiled, a series of thought-provoking questions are presented. These questions help categorize users into specific psychological traits, adding a personalized touch to their journaling experience.

Once a user is logged in and profiled, the application kicks into high gear. It begins capturing input for journal entries, which serve as the foundation for the enchanting "magic journals." These magical journals take real-life experiences and infuse them with a touch of AI creativity. Each journal entry is transformed into a captivating short story, complemented by an AI-generated image that brings the tale to life.

Users have the power to curate their magic journals by transforming individual entries and then crafting a meta-history featuring all the fantastic short stories. The culmination is a final, wholesome story that provides a positive and empowering recap of the user's month. This imaginative approach fosters a deep connection between the user and the stories, offering a unique perspective and mitigating feelings of helplessness.

Tellatale isn't just a psychological resource; it's a tool designed to inspire users to engage in reflective writing, reshaping their perceptions of daily experiences. Research has shown that how we remember and interpret our lives profoundly impacts our well-being and defines our identity. Tellatale is here to redefine your journaling experience, making it not just a record but a journey of self-discovery and positivity.


## Overview

This project consists of a capstone application with various modules for processing and interacting with user data. The project was intended to work as a  FastAPI endpoint that connects with the frontend. For this demo the only working script is langchain.py that can be executed with

``` 
python src/langchain.py
``` 

This project works with python=3.10
You can install this python version with

``` 
conda install python=3.10
``` 

Once installed you can load the required libraries to execute this code by running
``` 
pip install -r requirements.txt 
``` 


## Table of Contents

- [Capstone Project](#capstone-project)
  - [Overview](#overview)
  - [Directory Structure](#directory-structure)
  - [Tools](#tools)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Notebook](#notebook)
  - [Requirements](#requirements)
  - [Contributing](#contributing)
  - [License](#license)

## Directory Structure

```plaintext
capstone_project/
│
├── brain_module.py
├── main.py
│
frontend/
├── build
├── node_modules
├── package-lock.json
├── package.json
├── public
└── src

notebook/
├── OpenAI_APIs.ipynb
├── Story_book.ipynb
├── config
├── coverage
└── resources

src/
├── agents
├── config
├── framework
├── frontend.py
├── langchhain.py
└── tools
