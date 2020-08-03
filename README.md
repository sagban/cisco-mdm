# Smart India Hackathon 2020: Team Kerberos
## AM291 Mid-Day Meal Analytics
## PSO: Cisco DEVNET
## Team members
- Sagar Bansal (L)
- Priyank Nagarnaik
- Shalaka Gedam
- Snigdha Patil
- Jeevant Pant
- Shashwat Kadam 

### Expected Problem Statement

As the Mid-Day Meal program runs in schools across the country, continuous auditing & monitoring of the program
might be challenging. Typical Auditing & Monitoring could involve:
- Ensuring number of students that took meal is same number reported.
- Lunch served is same as published/reported menu.
- Alerting in case of discrepancy and capability to centrally see past records / proof (numbers & visual) for any
school.
Student teams are expected to to explore the capabilities of Meraki camera’s inbuilt Machine learning (ML) modules
and develop solutions to monitor the activities under the Mid-day Meal Scheme.

### Modules :

1. Meraki MV Sense :
After connecting to the camera, MQTT broker subscribes to the topic on which the camera sends continuous video feed. The Meraki Raw Detection API is used for getting the person count. The timestamps for the URLs with the trigger person count greater than zero are stored. Using the Meraki Snapshot API, snapshot URL and its expiry are obtained. Thus, we get the number of students who got the meal. The URls are then sent for face recognition and food recognition respecively.

2. Person count :
The person count gives the number of students who got the meal using Meraki Raw Detection API.

3. Face recognition : 
The person count only ensures the number of students who got the meal. So, face recognition is important for reasons as follows :
	1. It ensures that every student registered with the Mid-Day-Meal Scheme gets food.
	2. When students come in a queue, there are chances that they will gather together near the serving area or students may come again in queue second time. So, here only taking the person count will create discrepancy as it will count the students again.  
	3. Unknown students/person taking meal can also be identified.
	Hence, face recognition is incorporated.
   
4. Food recognition :
	Food menu contains 4 items - roti, rice, dal and sabzi.
	The dataset is collected for these 4 classes. 
	Food is recognized from the image and is sent for comparison with the Mid-Day-Meal food menu.

5. Report generation :
	An elaborate report displays the following :
	1. the number of students who got the meal as counted by our analytics system and the count as reported by the school authorities.
	2. the food menu detected by our analytics system and the Mid-Day-Meal food menu. 
	3. displays the comparison between the reported data and the system's auditing and monitoring data.
	4. able to view the past records.

6. Alerting system :
	In case the student count and food menu does not match the expected, an alert will be sent to the system.
