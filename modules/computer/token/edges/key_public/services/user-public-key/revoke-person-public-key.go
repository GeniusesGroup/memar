/* For license and copyright information please see the LEGAL file in the code repository */

package upk

import (
	"memar/authorization"
	"memar/http"
	"memar/json"
	"memar/protocol"
	"memar/service"
	"memar/srpc"
)

var revokePersonPublicKeyService = service.Service{
	URN:                "urn:giti:sabz.city:service:revoke-person-public-key",
	Domain:             DomainName,
	ID:                 1649022441139197240,
	IssueDate:          1592390799,
	ExpiryDate:         0,
	ExpireInFavorOfURN: "",
	ExpireInFavorOfID:  0,
	Status:             protocol.Software_PreAlpha,

	Authorization: authorization.Service{
		CRUD:     authorization.CRUDUpdate,
		UserType: protocol.UserType_Person,
	},

	Name: map[protocol.LanguageID]string{
		protocol.LanguageEnglish: "RevokePersonPublicKey",
	},
	Description: map[protocol.LanguageID]string{
		protocol.LanguageEnglish: `Change status of public key and expire it. Due to legal history purpose never delete any public key.
PersonID in st.Connection.OwnerID same as stored one in datastore!
This service will check person authentication status force use OTP or not.`,
	},
	TAGS: []string{
		"PersonAuthentication",
	},

	SRPCHandler: RevokePersonPublicKeySRPC,
	ServeHTTP:   RevokePersonPublicKeyHTTP,
}

// RevokePersonPublicKeySRPC is sRPC handler of RevokePersonPublicKey service.
func RevokePersonPublicKeySRPC(st protocol.Stream) {
	var req = &revokePersonPublicKeyReq{}
	err = req.FromSyllab(srpc.GetPayload(st.IncomePayload))
	if err != nil {
		return
	}

	var res *revokePersonPublicKeyRes
	res, err = revokePersonPublicKey(st, req)
	// Check if any error occur in business logic
	if err != nil {
		return
	}

	st.OutcomePayload = make([]byte, srpc.MinLength+res.LenAsSyllab())
	res.ToSyllab(srpc.GetPayload(st.OutcomePayload))
}

// RevokePersonPublicKeyHTTP is HTTP handler of RevokePersonPublicKey service.
func RevokePersonPublicKeyHTTP(st protocol.Stream, httpReq *http.Request, httpRes *http.Response) {
	var req = &revokePersonPublicKeyReq{}
	err = req.FromJSON(httpReq.Body().Marshal())
	if err != nil {
		httpRes.SetStatus(http.StatusBadRequestCode, http.StatusBadRequestPhrase)
		return
	}

	var res *revokePersonPublicKeyRes
	res, err = revokePersonPublicKey(st, req)
	// Check if any error occur in business logic
	if err != nil {
		httpRes.SetStatus(http.StatusBadRequestCode, http.StatusBadRequestPhrase)
		return
	}

	httpRes.SetStatus(http.StatusOKCode, http.StatusOKPhrase)
	httpRes.SetBody(json.NewCodec(res))
}

type revokePersonPublicKeyReq struct {
	PublicKey [32]byte `valid:"PublicKey" json:",string"`
	Password  [32]byte `valid:"Password" json:",string"`
	OTP       uint32
}

type revokePersonPublicKeyRes struct{}

func revokePersonPublicKey(st protocol.Stream, req *revokePersonPublicKeyReq) (res *revokePersonPublicKeyRes, err protocol.Error) {
	err = st.Authorize()
	if err != nil {
		return
	}

	// Validate data here due to service use internally by other services!
	err = req.validator()
	if err != nil {
		return
	}

	res = &revokePersonPublicKeyRes{}

	return
}

func (req *revokePersonPublicKeyReq) validator() (err protocol.Error) {
	return
}

func (req *revokePersonPublicKeyReq) FromSyllab(payload []byte, stackIndex uint32) {
	return
}

func (req *revokePersonPublicKeyReq) FromJSON(payload []byte) (remaining []byte, err protocol.Error) {
	err = json.Unmarshal(buf, req)
	return
}

func (res *revokePersonPublicKeyRes) ToSyllab(payload []byte, stackIndex, heapIndex uint32) (freeHeapIndex uint32) {
}

func (res *revokePersonPublicKeyRes) LenOfSyllabStack() uint32 {
	return 0
}

func (res *revokePersonPublicKeyRes) LenOfSyllabHeap() (ln uint32) {
	return
}

func (res *revokePersonPublicKeyRes) LenAsSyllab() uint64 {
	return uint64(res.LenOfSyllabStack() + res.LenOfSyllabHeap())
}

func (res *revokePersonPublicKeyRes) ToJSON(payload []byte) (added []byte, err protocol.Error) {
	var encoder = json.Encoder{Buf: payload}

	buf, _ = json.Marshal(res)
	return
}
