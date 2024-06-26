import streamlit as st
import time

# Initialize session state for chat messages and step tracking
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'step' not in st.session_state:
    st.session_state.step = 1

# Function to display chat history
def display_chat():
    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.markdown(message['content'])

# Set up the chat
st.title("GamsatGPT")
st.subheader("Try this demo and see the kinds of questions and responses that can be generated.")

# Display chat history
display_chat()

if st.session_state.step == 1:
    # First user input
    if prompt := st.chat_input("Ask me to make you a question", key="first_input"):
        with st.chat_message("user"):
            st.markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})

        # Simulate a delay with spinner
        with st.spinner('Generating response...'):
            time.sleep(2)

        response = "Certainly, here is a response I generated earlier..."
        with st.chat_message("assistant"):
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Simulate a delay with spinner
        with st.spinner('Generating response...'):
            time.sleep(4)  # Simulate a delay of 4 seconds

        # Display text
        question = """
### Problem Stem ###

A new planet, Exo-415, was discovered in a distant galaxy and has caught the attention of astronomers due to its unique atmospheric composition and unusual gravitational forces. Exo-415 has a significantly higher proportion of methane ($CH_4$) than Earth, constituting approximately 40% of its atmosphere, followed by nitrogen ($N_2$) at 35%, and various trace gases making up the rest. Despite the high methane concentration, measurements have shown that the surface temperature of Exo-415 is lower than Earth's. Furthermore, this planet has a gravitational pull 1.5 times stronger than Earth's, suggesting a higher density.

Studies have also indicated that the planet's rotation period is quite short: a day on Exo-415 is only 6 hours long, which leads to extreme differences in temperature between the day and night sides. Researchers hypothesize that the rapid rotation might be influencing atmospheric dynamics in ways not seen on Earth. Additionally, the high methane levels have been linked to an unknown biological activity unique to Exo-415, showing a potential for extraterrestrial life.

With these observations in mind, consider the following hypotheses on why the surface temperature of Exo-415 is lower than that of Earth:

### Question ###

Which hypothesis most plausibly explains why the surface temperature of Exo-415 is lower than Earth's, despite the high methane concentration?
a) The high atmospheric methane concentration on Exo-415 suggests strong greenhouse effects, which should logically result in higher surface temperatures, contradicting the measurements.
b) The intense gravitational pull (1.5 times stronger than Earth's) compresses the atmosphere more, increasing its density, which might result in efficient heat radiation into space.
c) The rapid rotation of Exo-415 (6-hour days) could lead to severe winds, distributing heat unevenly and leading to cooler average temperatures.
d) The higher proportion of methane in combination with other trace gases could result in more efficient absorption and radiation of heat, maintaining a cooler overall temperature.

"""
        with st.chat_message("assistant"):
            st.markdown(question)
            st.session_state.messages.append({"role": "assistant", "content": question})

        # Provide a predefined response
        response = "After presenting the question, I would instruct you to look for evidence supporting or opposing answer A, before working through each of the other options. However, if you get stuck, I can help direct you towards relevant areas of them stem and ask you questions to prompt your critical thinking."
        with st.chat_message("assistant"):
            time.sleep(1)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

        with st.spinner('Generating response...'):
            time.sleep(2)
            
        response = "When you're ready, why don't you tell me you are stuck and need some help?"
        with st.chat_message("assistant"):
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        
        st.session_state.step = 2
        st.experimental_rerun()

elif st.session_state.step == 2:
    # Second user input
    if second_prompt := st.chat_input("Enter your reply here...", key="second_input"):
        with st.chat_message("user"):
            st.markdown(second_prompt)
            st.session_state.messages.append({"role": "user", "content": second_prompt})

        # Simulate a delay with spinner
        with st.spinner('Generating response...'):
            time.sleep(2)

        response = """
Ok, let's break down Option A.
Option A suggests that the high atmospheric methane concentration should result in stronger greenhouse effects, thus higher surface temperatures. Think about:
1. Methane's Role: Methane is a potent greenhouse gas. Typically, high concentrations of methane would trap more heat.
2. Contradiction with Evidence: The stem states that the surface temperature is lower than Earth's, which contradicts this idea.
Does this help you find evidence whether option A is supported or opposed?
"""
        with st.chat_message("assistant"):
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        
        st.session_state.step = 3
        st.experimental_rerun()

elif st.session_state.step == 3:
    # Third user input
    if third_prompt := st.chat_input("Enter your reply here...", key="third_input"):
        with st.chat_message("user"):
            st.markdown(third_prompt)
            st.session_state.messages.append({"role": "user", "content": third_prompt})

        # Simulate a delay with spinner
        with st.spinner('Generating response...'):
            time.sleep(2)

        response = """
Hopefully that helped direct your focus on which parts of the stem are relevant. We would then do a similar process with the other options to help you build your ability to critically evaluate the evidence provided.
After going through all of the options, I would ask you what you think the correct answer is, why don't you have a go?
"""
        with st.chat_message("assistant"):
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        st.session_state.step = 4
        st.experimental_rerun()

elif st.session_state.step == 4:
    # Fourth user input
    if fourth_prompt := st.chat_input("Enter your reply here...", key="fourth_input"):
        with st.chat_message("user"):
            st.markdown(fourth_prompt)
            st.session_state.messages.append({"role": "user", "content": fourth_prompt})

        # Simulate a delay with spinner
        with st.spinner('Generating response...'):
            time.sleep(4)

        response = """
## Detailed Response ## 

**Correct answer: Option C**
### Evidence for Option C: ###

The rapid rotation of Exo-415 might produce severe winds and atmospheric dynamics that could spread heat unevenly across the planet, leading to lower average temperatures, despite high daytime temperatures.
Evidence against each option:

1. Option A:

    * Against: Methane is known for its greenhouse effect which should increase surface temperatures, contrary to the lower measurements.

2. Option B:
    
    * Against: The argument relies on the denser atmosphere leading to efficient heat radiation, which is an indirect and less intuitive connection.

3. Option D:

    * Against: Methane's greenhouse effect complicates this explanation. While interactions with other gases could be complex, there's no direct evidence in the stem for this specific interaction leading to cooler temperatures.

I would conclude my response by asking if you struggled with anything in this question or if you would you like tips for improvement? Why don't you ask me for some tips?
"""
        with st.chat_message("assistant"):
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

        st.session_state.step = 5
        st.experimental_rerun()

elif st.session_state.step == 5:
    # Final user input
    if final_prompt := st.chat_input("Enter your reply here...", key="final_input"):
        with st.chat_message("user"):
            st.markdown(final_prompt)
            st.session_state.messages.append({"role": "user", "content": final_prompt})

        # Simulate a delay with spinner
        with st.spinner('Generating response...'):
            time.sleep(4)

        response = """
Certainly, here are some tips to enhance your critical thinking skills and tackle these challenging questions more effectively:
### Tips for Improvement ###

1. Break Down the Stem:
    * Carefully read the entire problem stem. Identify key pieces of information and how they might relate to each other.
    * Summarize complex information. For example, jot down relevant points like atmospheric composition, gravitational pull, rotation period, and any unique phenomena like biological activity.
2. Evaluate Each Option Separately:
    * For each multiple-choice option, compare it directly with evidence presented in the stem. Ask yourself how the information supports or opposes the given option.
    * Look for explicit and implicit clues. Some evidence might not directly state the answer but implies it through logical connections.
3. Consider Contradictions:
    * If an option seems reasonable at first glance, double-check to see if any stem information directly contradicts it. This helps eliminate options more confidently.
    * Understand the natural behaviors of scientific concepts (like methane's greenhouse effect) and see if the option aligns logically with these well-known behaviors.
4. Synthesize Information:
    * Often, multiple pieces of information need to be combined to reach a conclusion. Practice connecting the dots between seemingly unrelated facts in the problem stem.
    * Construct a mental or written map of how different pieces of information interact.
5. Be Aware of Cognitive Biases:
    * Recognize common biases such as confirmation bias (favoring information that confirms preexisting beliefs) or the anchoring effect (overemphasis on an initial piece of information).
    * Approach each option with an open mind and consider it independently of your initial inclinations.
6. Take Your Time:
    * Rushing through complex questions often leads to oversight. Take time to thoroughly analyze each option and the corresponding evidence.
    * Practice patience and ensure you have considered all the presented information before making a decision.
### Practice Exercise ###

To reinforce these tips, try working through similar questions and consciously apply these strategies. Reflect on your thought process and where you might have missed critical evidence. Over time, this will help hone your reasoning skills.
"""
        with st.chat_message("assistant"):
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
