# Timeline

## Usage

- Recently viewed item such as movies, products, ...

## Idea backlog from edge code comments

Raw proposals from comment notes inside edge .go files (comments remain in code as source). Review discipline per [vocabulary-discipline.handoff.md](../vocabulary-discipline.handoff.md). Nothing below is ratified.

### Per-user timeline kinds - edges/user-relation-group.go
- **Idea**: user-timeline labels: PrivateTimeLine (home feed, for the user itself), PublicTimeLine (for others to see the user feed), LifeTimeLine, UserNotificationTimeline. Example form in comments: [User, Group, Label] >> [Omid, 123, Life TimeLine].
- **Review questions**: is a timeline a group node with kind labels, or distinct edge kinds? Do the kinds overlap the knowledge/content domain?

### Group chat timelines - edges/group-relation-group.go
- **Idea**: Chats_Staff and Chats_Customer labels (use for comments and similar content).
- **Review questions**: do these belong to the knowledge/content discussion threads instead?

### Event reasons - edges/event/protocol/dt-reason.go
- **Idea**: a full social-graph reason taxonomy for timeline events: Reason_UserMentioned; friendship-cycle reasons 1st-6th; Reason_UserFollow; FriendForward (retweet/forward), FriendReaction (liked...), FriendReplied, FriendReceivedAReply, FollowByFriend (usually 1st cycle); recommendation reasons BaseOnUserReaction / BaseOnUserFollow / BaseOnUserTopics / BaseOnUserFeedback / UserMightLike.
- **Review questions**: do the friendship-cycle reasons duplicate the derived connection-1st/2nd/3rd edges (see social_connections README)? Is the recommendation-reason set pluggable analytics rather than core timeline?