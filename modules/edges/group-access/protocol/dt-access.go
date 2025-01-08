/* For license and copyright information please see the LEGAL file in the code repository */

package cap

type Access uint8

const (
	Content_Access_Unset    Access = 0
	Content_Access_UserList Access = (1 << iota)
	Content_Access_Public
	Content_Access_RegisteredUser
	Content_Access_PremiumUser // usually charge for monthly access.  /// other plan?? basic, ... /// role based??
)
