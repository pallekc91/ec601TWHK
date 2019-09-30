# Lessons learned

* I like the the process that come up with the problem and then  solve it. For our project, we collect the tweets tagged our twitter account, and send the json file to Google  Natrual  Language API to analyze sentiemnt in every texts. Then we figure out which department it belongs to and trigger a email sender to send the email to relevant department.

* For the tweets collection part, we only got part of text for each sentence. The reason is that the twitter API we use can only display part of tweets and give a link if there are something unshown. Another improvement is the department identification part, because we only have few words related to each department in the dictionary. So the analysis result is not accurate in some way. We have to enlarge our dictionary or find a new way to get this done better.

* What I want to aviod next time is not to put all code together. Dividing code with the modules would be easier to modify code and easier to understand.
