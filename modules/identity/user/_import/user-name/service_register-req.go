/* For license and copyright information please see the LEGAL file in the code repository */

package services

import (
	"libgo/protocol"
)

// SetNameReq is the request structure of SetName()
type SetNameReq struct {
	UserID   string `valid:"userID"`
	Username string `valid:"username"`
}

// Username
// - Usernames must be at least 3 and no more than 63 characters long and unique in the application
// - Usernames must be a series of one or more labels. Adjacent labels are separated by a single period (.). Usernames can contain lowercase letters, numbers, and hyphens. Each label must start and end with a lowercase letter or a number.
// - Usernames must not be formatted as an IP address (e.g., 192.168.5.4).
// - We recommend that you do not use periods (".") in usernames.
// - The following examples are valid usernames:
//   - myawsbucket
//   - my.aws.bucket
//   - myawsbucket.1
//
// - The following examples are invalid usernames:
//   - .myawsbucket	usernames cannot start with a period (.).
//   - myawsbucket.	usernames cannot end with a period (.).
//   - my..examplebucket	There can be only one period between labels.
//
// Users have limit to change their username from set date!
var rrv registerRequestValidation

type registerRequestValidation struct{}

func (v *registerRequestValidation) validateUsername(u string) protocol.Error {
	return nil
}
