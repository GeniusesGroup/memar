/* For license and copyright information please see the LEGAL file in the code repository */

package gap

type JoinWay uint8

const (
	JoinWay_Unset JoinWay = iota
	JoinWay_Direct
	JoinWay_JoinLink
	JoinWay_Invite
)
