# Wanted components
Lightweight LED displays for Raspberry Pi x3 (maybe spare)

Powerful servos x8 or similar

Raspberry Pi 5 x1

Camera for Raspberry Pi x1

# User Story
- User sits in front of the device and switches it on
- If user signed "new"
	- Robot generates new word/phrase
	- Robot shows word/phrase on face for a few seconds
	- Robot signs word/phrase
	- Repeat show and sign 2 more times
	- Wait for user to attempt sign
	- If user signed for repeat then repeat
	- If user signs correctly then success dance and exit conditional
	- If user signs incorrectly for fifth time then be sad and exit conditional
	- If user signs incorrectly then be sad and go back to show and sign
- If user signed "practice"
	- Robot generates word/phrse from previously learned set
	- Robot shows word/phrase on face for a few seconds
	- Robot signs word/phrase
	- Repeat show and sign 2 more times
	- Wait for user to attempt sign
	- If user signed for repeat then repeat
	- If user signs correctly then success dance and exit conditional
	- If user signs incorrectly for fifth time then be sad and exit conditional
	- If user signs incorrectly then be sad and go back to show and sign

## Interaction model
Interaction is done via a camera on the device that faces the user. When the user attempts a BSL gesture the camera should capture it and check its similarity to either a key interaction gesture ("new" or "practice") or the word/phrase being singed by the device.

# Other similar devices
There are a few sign-language robots on the market, but most are for research purposes, have many complex degrees of freedom in their movements, and sign other dialects of sign language such as ASL or PSL.

# Unique Selling Point
It is unique - there are no other devices this simple that can perform sign language, and none that can for BSL.