/* For license and copyright information please see the LEGAL file in the code repository */

package event_p

type Reason uint8

const (
	Reason_Unset Reason = iota
	Reason_UserMentioned

	Reason_1stFriendshipCycle // new comment from friend of user
	Reason_2stFriendshipCycle
	Reason_3stFriendshipCycle
	Reason_4stFriendshipCycle
	Reason_5stFriendshipCycle
	Reason_6stFriendshipCycle
	Reason_UserFollow // just user follow other, not any friend relationship

	Reason_FriendForward        // retweet or forward other comment to the user timeline
	Reason_FriendReaction       // interest domain:  Liked, ...
	Reason_FriendReplied        // new comment to a user comment
	Reason_FriendReceivedAReply // a friend of user received a reply
	Reason_FollowByFriend       // usually 1stFriendshipCycle

	Reason_BaseOnUserReaction
	Reason_BaseOnUserFollow
	Reason_BaseOnUserTopics
	Reason_BaseOnUserFeedback
	Reason_UserMightLike
)
