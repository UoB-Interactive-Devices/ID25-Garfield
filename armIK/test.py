from ikpy.chain import Chain
from ikpy.link import OriginLink, URDFLink
import numpy as np
import ikpy.utils.plot as plot_utils
import time
from adafruit_servokit import ServoKit 

# pca = ServoKit(channels=16)

right_arm_chain = Chain(name='right_arm', links=[
    OriginLink(),
    URDFLink(
      name="shoulder1",
      origin_translation=[0, 0, 0],
      origin_orientation=[0, 0, 0],
      rotation=[1, 0, 0],
    ),
    URDFLink(
        name="shoulder2",
        origin_translation=[2,0,0],
        origin_orientation=[0,0,0],
        rotation=[0,1,0]
    ),
    URDFLink(
      name="elbow",
      origin_translation=[8.5, 0, 0],
      origin_orientation=[0, 0, 0],
      rotation=[0, 1, 0],
    ),
    URDFLink(
      name="wrist",
      origin_translation=[8.5, 0, 0],
      origin_orientation=[0, 0, 0],
      rotation=[0, 1, 0],
    ),
    URDFLink(
      name="hand",
      origin_translation=[7.5, 0, 0],
      origin_orientation=[0, 0, 0],
      rotation=[0, 1, 0],
    )
])

# left_arm_chain = Chain(name='right_arm', links=[
#     OriginLink(),
#     URDFLink(
#       name="shoulder1",
#       origin_translation=[0, 0, 0],
#       origin_orientation=[0, 0, 0],
#       rotation=[1, 0, 0],
#     ),
#     URDFLink(
#         name="shoulder2",
#         origin_translation=[-2,0,0],
#         origin_orientation=[0,0,0],
#         rotation=[0,1,0]
#     ),
#     URDFLink(
#       name="elbow",
#       origin_translation=[-8.5, 0, 0],
#       origin_orientation=[0, 0, 0],
#       rotation=[0, 1, 0],
#     ),
#     URDFLink(
#       name="wrist",
#       origin_translation=[-8.5, 0, 0],
#       origin_orientation=[0, 0, 0],
#       rotation=[0, 1, 0],
#     ),
#     URDFLink(
#       name="hand",
#       origin_translation=[-7.5, 0, 0],
#       origin_orientation=[0, 0, 0],
#       rotation=[0, 1, 0],
#     )
# ])

def custom_clamp(x,minv,maxv):
    if (x < minv):
        print("Clamping: ", x, " less than min value ", minv)
        return minv
    if (x > maxv):
        print("Clamping: ", x, " greater than max value ", maxv)
        return maxv
    else:
        return x

class moment:
  def __init__(self, position, hands, delay):
    self.position = position
    self.hands = hands
    self.delay = delay
class gesture :
  # def __init__(self, positions, hands, face, times):
  #   assert(len(positions) == len(hands) == len(times))
  #   gestureVec = []
  #   for i in range (len(positions)):
  #     gestureVec.append(moment(positions[i], hands[i], delay[i]))
    # self.list = gestureVec
  def __init__(self, moments):
    self.list = moments
      
def move_arm(chain, position1, position2, time):
    startIK = chain.inverse_kinematics(position1)
    endIK = chain.inverse_kinematics(position2)
    chain.plot(startIK, ax)
    chain.plot(endIK, ax)
    for t in range(time*10):
      for i, startjoint in enumerate(startIK):
          startpos = (startjoint + np.pi)/(2*np.pi)
          endjoint = endIK[i]
          endpos = (endjoint + np.pi)/(2*np.pi)
          diff = endpos - startpos
          pos = startpos + diff*(t / (time * 10))
          print("JOINT POSITITON:",i, ": ", pos)
          # pca.servo[i].fraction = custom_clamp(pos,0,1) 
    print(startIK)
    print(endIK)
  
def do_gesture(gesture):
  for moment in gesture.list:
    move_arm(left_arm_chain, moment.position[0])
    move_arm(right_arm_chain, moment.position[1])
    time.sleep(moment.delay)

import matplotlib.pyplot
from mpl_toolkits.mplot3d import Axes3D
ax = matplotlib.pyplot.figure().add_subplot(111, projection='3d')
# start = moment((np.array([5,0,0]), np.array([5,5,5])), (1,1), 0)
# end = moment((np.array([-5,0,0]), np.array([-5,-5,-5])), (1,1), 1)
# moments = [start,end]
# gesture = gesture(moments)
# do_gesture(gesture)
start = np.array([-15,0,0])
end = np.array([0,-15,-15])
move_arm(right_arm_chain, start, end, 5)
matplotlib.pyplot.show()


# if __name__ == '__main__':
#     init()
#    main()
