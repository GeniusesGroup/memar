/* For license and copyright information please see the LEGAL file in the code repository */

package pa

import (
	"crypto/sha512"

	"libgo/authorization"
	"libgo/http"
	"libgo/json"
	"libgo/otp"
	"libgo/protocol"
	"libgo/service"
	"libgo/srpc"
	"libgo/syllab"
)

var recoverPersonAccountService = service.Service{
	URN:                "urn:giti:sabz.city:service:recover-person-account",
	Domain:             DomainName,
	ID:                 1768405648906652869,
	IssueDate:          1592390624,
	ExpiryDate:         0,
	ExpireInFavorOfURN: "",
	ExpireInFavorOfID:  0,
	Status:             protocol.Software_PreAlpha,

	Authorization: authorization.Service{
		CRUD:     authorization.CRUDUpdate,
		UserType: protocol.UserType_All ^ protocol.UserType_Unset,
	},

	Name: map[protocol.LanguageID]string{
		protocol.LanguageEnglish: "RecoverPersonAccount",
	},
	Description: map[protocol.LanguageID]string{
		protocol.LanguageEnglish: `Recover user account due to lost password or lost all active devices with active connection!
If user authenticated successfully in st.Connection.PeerThingID one time before can recover just by OTP
Otherwise must send all information (OTP && SecurityKeyOTP) to recover!
It will change user status to PersonNotForceUse2Factor!`,
	},
	TAGS: []string{
		"PersonAuthentication",
	},

	SRPCHandler: RecoverPersonAccountSRPC,
	ServeHTTP:   RecoverPersonAccountHTTP,
}

// RecoverPersonAccountSRPC is sRPC handler of RecoverPersonAccount service.
func RecoverPersonAccountSRPC(st protocol.Stream) {
	var req = &recoverPersonAccountReq{}
	err = req.FromSyllab(srpc.GetPayload(st.IncomePayload))
	if err != nil {
		return
	}

	err = recoverPersonAccount(st, req)
	// Check if any error occur in business logic
	if err != nil {
		return
	}

	st.OutcomePayload = make([]byte, srpc.MinLength)
}

// RecoverPersonAccountHTTP is HTTP handler of RecoverPersonAccount service.
func RecoverPersonAccountHTTP(st protocol.Stream, httpReq *http.Request, httpRes *http.Response) {
	var req = &recoverPersonAccountReq{}
	err = req.FromJSON(httpReq.Body().Marshal())
	if err != nil {
		httpRes.SetStatus(http.StatusBadRequestCode, http.StatusBadRequestPhrase)
		return
	}

	err = recoverPersonAccount(st, req)
	// Check if any error occur in business logic
	if err != nil {
		httpRes.SetStatus(http.StatusBadRequestCode, http.StatusBadRequestPhrase)
		return
	}

	httpRes.SetStatus(http.StatusOKCode, http.StatusOKPhrase)
}

type recoverPersonAccountReq struct {
	PersonID     [32]byte `json:",string"` // UUID of registered user
	PhoneNumber  uint64
	PhoneOTP     uint64
	OTP          uint64
	PasswordHash [32]byte `json:",string"`
	SecurityKey  [32]byte `json:",string"`
}

func recoverPersonAccount(st protocol.Stream, req *recoverPersonAccountReq) (err protocol.Error) {
	err = st.Authorize()
	if err != nil {
		return
	}

	var otpReq = otp.GenerateTimeOTPReq{
		Hasher:     sha512.New512_256(),
		SecretKey:  smsOTPSecurityKey,
		Additional: make([]byte, 8),
		Period:     smsOTPPeriod,
		Digits:     smsOTPDigits,
	}
	syllab.SetUInt64(otpReq.Additional, 0, req.PhoneNumber)
	var timeOTP uint64
	timeOTP, err = otp.GenerateTimeOTP(&otpReq)
	if err != nil {
		return
	}

	if req.PhoneOTP != timeOTP {

		return

	}

	var pa = data.PersonAuthentication{
		PersonID: req.PersonID,
	}
	pa.GetLastByPersonID()

	return
}

func (req *recoverPersonAccountReq) validator() (err protocol.Error) {
	return
}

func (req *recoverPersonAccountReq) FromSyllab(payload []byte, stackIndex uint32) {
	return
}

func (req *recoverPersonAccountReq) FromJSON(payload []byte) (remaining []byte, err protocol.Error) {
	err = json.Unmarshal(buf, req)
	return
}
