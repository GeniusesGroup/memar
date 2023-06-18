/* For license and copyright information please see the LEGAL file in the code repository */

package thp

import (
	"libgo/protocol"

	cp "org/modules/comment/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
// home timeline feed
type DataModel interface {
	UserID() up.UserUUID         //
	CommentID() cp.CommentUUID   //
	ReasonUserID() up.UserUUID   // it can be the owner of comment or any other user base on reason
	Reason() HomeTimeline_Reason //
	SaveTime() protocol.Time     //
	// TODO::: node details??
}

type HomeTimeline_Reason uint8

const (
	HomeTimeline_Reason_Unset HomeTimeline_Reason = iota
	HomeTimeline_Reason_UserMentioned

	HomeTimeline_Reason_1stFriendshipCycle // new comment from friend of user
	HomeTimeline_Reason_2stFriendshipCycle
	HomeTimeline_Reason_3stFriendshipCycle
	HomeTimeline_Reason_4stFriendshipCycle
	HomeTimeline_Reason_5stFriendshipCycle
	HomeTimeline_Reason_6stFriendshipCycle
	HomeTimeline_Reason_UserFollow // just user follow other, not any friend relationship

	HomeTimeline_Reason_FriendForward        // retweet or forward other comment to the user timeline
	HomeTimeline_Reason_FriendReaction       // interest domain:  Liked, ...
	HomeTimeline_Reason_FriendReplied        // new comment to a user comment
	HomeTimeline_Reason_FriendReceivedAReply // a friend of user received a reply
	HomeTimeline_Reason_FollowByFriend       // usually 1stFriendshipCycle

	HomeTimeline_Reason_BaseOnUserReaction
	HomeTimeline_Reason_BaseOnUserFollow
	HomeTimeline_Reason_BaseOnUserTopics
	HomeTimeline_Reason_BaseOnUserFeedback
	HomeTimeline_Reason_UserMightLike
)

type (
	HomeTimeline_Services_Register_Request  interface{}
	HomeTimeline_Services_Register_Response interface{}
)
