/* For license and copyright information please see the LEGAL file in the code repository */

package org

/*
# Foreign nations platform information service
Cache all foreign fundamental user data in this service.

## Manual add foreign data
### Verifying data
Use mobile||email||...+time to generate otp code to verify mobile||email||... . OTP created must have expire time(max 15 minute)

### Authorization Data
User can set authorization level to each data in this service. We must use relations MS to detect level of user related to owner. relations have multi level e.g. family, friend, friend of freind, ...
user can access other user if he/she is in min access level.
*/

// ForeignDetail is the storing struct of platforms access data
// We must get needed data to improve our AI.
type UserOtherAppCache interface {
	UserOtherAppID() [16]byte          // user-other-app domain
	UserID() [16]byte     // user-status domain
	PlatformID       [4]byte // Country e.g. Iran, ... || Digital platforms e.g. Instagram, Facebook, Google, Github, Yahoo, ...
	DelegateToken    [16]byte
	AccessToken      [16]byte
	// Data below cache data from other platfrom or manually store user data
	UUID          string // Country national code or UserID in digital platforms
	Gender        string // In ISO format
	PassportID    string // If exist mean user have that country Nationality
	Surename      string
	Middlename    string
	Givenname     string
	Nickname      string
	Username      string
	EmailURI      string
	Website       string
	Phone         uint64
	TaxID         string
	LocationID    string
	PostalCode    string
	DateOfBirth   uint64
	PlaceOfBirth  string
	PassportImage [16]byte // Object UUID
	VerifiedDate  uint64   // If !=0 user get famous blue badge(tick) like instagram, twitter,...
}

type User interface {
	ID() [16]byte
	Firstname() string
	Lastname() string
	Gender() string
	BirthDate() [8]uint
	Bio() string
}

type UserService interface {
	GetUser(userID [16]byte) (User, error)
	SetUser(user User) error
}

const (
	UserDomain = "user.protocol"

	UserService = "urn:giti:user.protocol:service:"
)

// below structure just use in static data show like QR-Code images not services
// https://openid.net/specs/openid-connect-core-1_0.html
const (
	UserIDURN     = "urn:user:id:{{...}}"
	UserNameURN   = "urn:user:name:{{...}}"
	UserNumberURN = "urn:user:number:{{...}}"
)
