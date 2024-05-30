import streamlit as st
import time

# Initialize session state for chat messages and step tracking
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'intro_displayed' not in st.session_state:
    st.session_state.intro_displayed = False

# Function to display chat history
def display_chat():
    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.markdown(message['content'])

# Set up the chat
st.title("GamsatGPT")
st.subheader("Why don't you try out this demo and ask me to make you a question?")

# Display intro message if not already displayed
if not st.session_state.intro_displayed:
    with st.chat_message("assistant"):
        intro = "This is an automated demo, I'll show you an example of a question that I generated as well as how you can interact with me"
        st.markdown(intro)
        st.session_state.messages.append({"role": "assistant", "content": intro})
    st.session_state.intro_displayed = True

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
            time.sleep(1)

        response = "Certainly, here is a response I generated earlier..."
        with st.chat_message("assistant"):
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Simulate a delay with spinner
        with st.spinner('Generating response...'):
            time.sleep(4)  # Simulate a delay of 4 seconds

        # Display text
        question = """
Given these conditions, consider the effects of depolarizing noise on the entanglement of photon pairs and their subsequent measurement outcomes. Furthermore, analyze how these influences align with various quantum mechanical principles and interpretations, including the collapse of the wavefunction and non-locality.

## Question ##
Given the experimental conditions described, which of the following statements is most likely correct regarding the correlation of measurement outcomes at locations A and B?

#### Options: ####
A. If the depolarizing noise parameter 𝑝 is high, the measurement outcomes at A and B will show no correlation.

B. Regardless of the depolarizing noise parameter 𝑝, the measurement outcomes at A and B will remain perfectly correlated due to the nature of entanglement.

C. The correlation between the measurement outcomes at A and B decreases as the depolarizing noise parameter 𝑝 increases, but does not completely disappear even at 𝑝=1.

D. If the depolarizing noise parameter 𝑝 is low, the measurement outcomes at A and B will be perfectly correlated, but as 𝑝 increases, these correlations diminish and eventually become random.

Can you find any evidence supporting or opposing option A?
"""
        with st.chat_message("assistant"):
            st.markdown(question)
            st.session_state.messages.append({"role": "assistant", "content": question})

        # Provide a predefined response
        response = "After presenting the question, I would instruct you to look for evidence supporting or opposing answer A, before working through each of the other options."
        with st.chat_message("assistant"):
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

        with st.spinner('Generating response...'):
            time.sleep(3)
            
        response = "However, if you get stuck, I can help direct you towards relevant areas of them stem and ask you questions to prompt your critical thinking. When you're ready, why don't you tell me you are stuck and need some help?"
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
Hopefully that helped, we would then do a similar process with the other options to help you build your ability to critically evaluate the evidence provided.
After going through all of the options, I would ask you what you think the correct answer is, and generate something like this...
"""
        with st.chat_message("assistant"):
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Simulate a delay with spinner
        with st.spinner('Generating response...'):
            time.sleep(4)
    
        response = """
## Detailed Response ## 

**Correct answer: Option C**
### Evidence for Option C: ###

* The rapid rotation of Exo-415 might produce severe winds and atmospheric dynamics that could spread heat unevenly across the planet, leading to lower average temperatures, despite high daytime temperatures.
Evidence against each option:

**1. Option A:**
    * Against: Methane is known for its greenhouse effect which should increase surface temperatures, contrary to the lower measurements.
**2. Option B:**
    * Against: The argument relies on the denser atmosphere leading to efficient heat radiation, which is an indirect and less intuitive connection.
**3. Option D:**
    * Against: Methane's greenhouse effect complicates this explanation. While interactions with other gases could be complex, there's no direct evidence in the stem for this specific interaction leading to cooler temperatures.

I would conclude my response by asking if you struggled with anything in this question or if you would you like tips for improvement? Why don't you ask me for some tips?
"""
        with st.chat_message("assistant"):
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

        st.session_state.step = 4
        st.experimental_rerun()

elif st.session_state.step == 4:
    # Final user input
    if final_prompt := st.chat_input("Enter your reply here...", key="final_input"):
        with st.chat_message("user"):
            st.markdown(final_prompt)
            st.session_state.messages.append({"role": "user", "content": final_prompt})

        # Simulate a delay with spinner
        with st.spinner('Generating response...'):
            time.sleep(3)

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
