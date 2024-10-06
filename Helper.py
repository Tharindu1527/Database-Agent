from sqlalchemy import create_engine
import pandas as pd

#path to your SQLite database file
database_file_path = "LLM_AGENT.sql"

#create an engine to connect to the MYSQL database
engine = create_engine("mysql+mysqldb://THARINDU:Tha15270@localhost/LLM_AGENT") #you have to create user :THARINDU and use your schema like LLM_AGENT 
file_url = "all-states-history.csv"
df = pd.read_csv("all-states-history.csv").fillna(value = 0)
df.to_sql(      #connect csv file to mysql database
    'all_states_history',
    con=engine,
    if_exists='replace',
    index=False
)


tools_sql = [
    {
        "type": "function",
        "function": {
            "name": "get_hospitalized_increase_for_state_on_date",
            "description": "Retrieves the daily increase in hospitalizations for a specific state on a specific date.",
            "parameters": {
                "type": "object",
                "properties": {
                    "state_abbr": {
                        "type": "string",
                        "description": "The abbreviation of the state (e.g., 'NY', 'CA')."
                    },
                    "specific_date": {
                        "type": "string",
                        "description": "The specific date for the query in 'YYYY-MM-DD' format."
                    }
                },
                "required": ["state_abbr", "specific_date"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_positive_cases_for_state_on_date",
            "description": "Retrieves the daily increase in positive cases for a specific state on a specific date.",
            "parameters": {
                "type": "object",
                "properties": {
                    "state_abbr": {
                        "type": "string",
                        "description": "The abbreviation of the state (e.g., 'NY', 'CA')."
                    },
                    "specific_date": {
                        "type": "string",
                        "description": "The specific date for the query in 'YYYY-MM-DD' format."
                    }
                },
                "required": ["state_abbr", "specific_date"]
            }
        }
    }
]



# define functions
import numpy as np
def get_hospitalized_increase_for_state_on_date(state_abbr, specific_date):
    try:
        query = f"""
        SELECT date, hospitalizedIncrease
        FROM all_states_history
        WHERE state = '{state_abbr}' AND date = '{specific_date}';
        """
        with engine.connect() as connection:
            result = pd.read_sql_query(query, connection)
        if not result.empty:
            return result.to_dict('records')[0]
        else:
            return np.nan
    except Exception as e:
        print(e)
        return np.nan

def get_positive_cases_for_state_on_date(state_abbr, specific_date):
    try:
        query = f"""
        SELECT date, state, positiveIncrease AS positive_cases
        FROM all_states_history
        WHERE state = '{state_abbr}' AND date = '{specific_date}';
        """
        with engine.connect() as connection:
            result = pd.read_sql_query(query, connection)
        if not result.empty:
            return result.to_dict('records')[0]
        else:
            return np.nan
    except Exception as e:
        print(e)
        return np.nan



