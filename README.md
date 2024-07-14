# 🚀Motivation🚀
This project was developed with the goal to learn about API-Requests and Alexa skill development

# 🤖Simplified Explanation of how it works
1. Alexa gets an intent from the User to launch the skill
2. Alexa identifies the desired destination and calls "JourneyDuration.main()"
3. JourneyDuration sends a request to rmv-api, at first the response is processed only process for the duration of the Journey
4. Alexa asks if the user wishes for more information
5. If so "TravelDetails.main()" is called to further process the response and provide a detailed trip plan. Otherwise, the session ends.

# 📝Result examples
![RESULTS](https://cdn.discordapp.com/attachments/587739697216749589/1262103722658365480/Unbenannt.png?ex=66956130&is=66940fb0&hm=e0c6171760496a2bf63bf380427207e57540026641c367628960a96d1aa42168&)

# ⚠️Limitations of this Repository
Most of the Alexa-related components are handled on the Alexa skill development platform and not uploaded in this Repository.
