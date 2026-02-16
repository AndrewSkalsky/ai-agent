import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
from prompts import system_prompt
from functions.call_function_def import available_functions
from functions.call_function import call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key is None:
    raise RuntimeError("Missing api_key")

client = genai.Client(api_key=api_key)

def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    # Now we can access `args.user_prompt`

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    
    for _ in range(20):
        response = client.models.generate_content(
            model='gemini-2.5-flash'
            , contents=messages
            , config=types.GenerateContentConfig(
                tools=[available_functions]
                ,system_instruction=system_prompt
                ,temperature=0
                )
        )
        if response.usage_metadata is None:
            raise RuntimeError("invalid AI response")
            
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        
        for candidate in response.candidates:
            messages.append(candidate.content)
        
        if not response.function_calls:
            print(response.text)
            return

        functions_responses = []
        for f_call in response.function_calls:
            # print(f"Calling function: {f_call.name}({f_call.args})")
            function_call_result = call_function(f_call,args.verbose)
            if len(function_call_result.parts) == 0:
                raise Exception("Empty parts in function_call_result")
            if function_call_result.parts[0].function_response == None:
                raise Exception("Function response is None")
            if function_call_result.parts[0].function_response.response == None:
                raise Exception("Missing response")
            functions_responses.append(function_call_result.parts[0])
            messages.append(function_call_result)
            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
    
    print("Loop reachded its limit. No final conclusion. Exiting...")
    exit(1)
            

if __name__ == "__main__":
    main()
