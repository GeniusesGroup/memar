/* For license and copyright information please see the LEGAL file in the code repository */

package label

// PersonPassword statuses
const (
	// authenticate person with Password + OTP
	Status_ForceUse2Factor = iota
	// user must change password and otp key(if enabled) for some reason
	Status_MustChangePassword
	// user can't use or decide to prevent authenticate via password with or without OTP.
	Status_DenyPasswordAuthentication
)
