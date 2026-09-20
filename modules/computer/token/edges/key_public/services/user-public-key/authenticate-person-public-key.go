/* For license and copyright information please see the LEGAL file in the code repository */

package upk

import (
	"memar/authorization"
	"memar/http"
	"memar/json"
	"memar/protocol"
	"memar/srpc"
)

var authenticatePersonPublicKeyService = service.Service{
	URN:                "urn:giti:sabz.city:service:authenticate-person-public-key",
	Domain:             DomainName,
	ID:                 16845460193864472411,
	IssueDate:          1592379653,
	ExpiryDate:         0,
	ExpireInFavorOfURN: "",
	ExpireInFavorOfID:  0,
	Status:             protocol.Software_PreAlpha,

	Authorization: authorization.Service{
		CRUD:     authorization.CRUDCreate,
		UserType: protocol.UserType_All,
	},

	Detail: map[protocol.LanguageID]service.ServiceDetail{
		Name:        "AuthenticatePersonPublicKey",
		Description: "Authenticate user and store given PublicKey to use by user for any purpose!",
		TAGS:        []string{"Authentication"},
	},

	SRPCHandler: AuthenticatePersonPublicKeySRPC,
	ServeHTTP:   AuthenticatePersonPublicKeyHTTP,
}

// AuthenticatePersonPublicKeySRPC is sRPC handler of AuthenticatePersonPublicKey service.
func AuthenticatePersonPublicKeySRPC(st protocol.Stream) {
	var req = &authenticatePersonPublicKeyReq{}
	err = req.FromSyllab(srpc.GetPayload(st.IncomePayload))
	if err != nil {
		return
	}

	var res *authenticatePersonPublicKeyRes
	res, err = authenticatePersonPublicKey(st, req)
	// Check if any error occur in business logic
	if err != nil {
		return
	}

	st.OutcomePayload = make([]byte, srpc.MinLength+res.LenAsSyllab())
	res.ToSyllab(srpc.GetPayload(st.OutcomePayload))
}

// AuthenticatePersonPublicKeyHTTP is HTTP handler of AuthenticatePersonPublicKey service.
func AuthenticatePersonPublicKeyHTTP(st protocol.Stream, httpReq *http.Request, httpRes *http.Response) {
	var req = &authenticatePersonPublicKeyReq{}
	err = req.FromJSON(httpReq.Body().Marshal())
	if err != nil {
		httpRes.SetStatus(http.StatusBadRequestCode, http.StatusBadRequestPhrase)
		return
	}

	var res *authenticatePersonPublicKeyRes
	res, err = authenticatePersonPublicKey(st, req)
	// Check if any error occur in business logic
	if err != nil {
		httpRes.SetStatus(http.StatusBadRequestCode, http.StatusBadRequestPhrase)
		return
	}

	httpRes.Body, err = res.ToJSON()
	// err make occur on just memory full!

	httpRes.SetStatus(http.StatusOKCode, http.StatusOKPhrase)
}

type authenticatePersonPublicKeyReq struct {
	PersonID     [32]byte `json:",string"`
	PasswordHash [32]byte `json:",string"`
	OTP          uint32
	PublicKey    [32]byte `json:",string"`
	ExpireAt     uint64
	CaptchaID    [16]byte `json:",string"`
}

type authenticatePersonPublicKeyRes struct{}

func authenticatePersonPublicKey(st protocol.Stream, req *authenticatePersonPublicKeyReq) (res *authenticatePersonPublicKeyRes, err protocol.Error) {
	// TODO::: Authenticate request first by service policy.

	err = st.Authorize()
	if err != nil {
		return
	}

	// Request should send with UserID! Otherwise use identification||information service to find UserID.

	// get ThingID from st.Connection.PeerThingID

	// Person can have one PublicKey on same thing! so if other active public key is exist for requested thing,
	// we should notify user and get confirmed. If user not access to any their active connection, user must do recovery proccess first.

	// Notify user about failed authenticated proccess!

	res = &authenticatePersonPublicKeyRes{}

	return
}

/*
	Request Encoders & Decoders
*/

func (req *authenticatePersonPublicKeyReq) FromSyllab(payload []byte, stackIndex uint32) {
	return
}

func (req *authenticatePersonPublicKeyReq) FromJSON(payload []byte) (remaining []byte, err protocol.Error) {
	err = json.Unmarshal(buf, req)
	return
}

/*
	Response Encoders & Decoders
*/

func (res *authenticatePersonPublicKeyRes) ToSyllab(payload []byte, stackIndex, heapIndex uint32) (freeHeapIndex uint32) {
	return
}

func (res *authenticatePersonPublicKeyRes) LenOfSyllabStack() uint32 {
	return 0
}

func (res *authenticatePersonPublicKeyRes) LenOfSyllabHeap() (ln uint32) {
	return
}

func (res *authenticatePersonPublicKeyRes) LenAsSyllab() uint64 {
	return uint64(res.LenOfSyllabStack() + res.LenOfSyllabHeap())
}

func (res *authenticatePersonPublicKeyRes) ToJSON() (buf []byte, err protocol.Error) {
	buf, err = json.Marshal(res)
	return
}
