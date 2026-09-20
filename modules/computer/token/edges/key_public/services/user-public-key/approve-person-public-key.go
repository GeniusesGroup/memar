/* For license and copyright information please see the LEGAL file in the code repository */

package upk

import (
	"memar/authorization"
	"memar/http"
	"memar/json"
	"memar/protocol"
	"memar/srpc"
	"memar/syllab"
)

var approvePersonPublicKeyService = service.Service{
	URN:                "urn:giti:sabz.city:service:approve-person-public-key",
	Domain:             DomainName,
	ID:                 7869575413726160909,
	IssueDate:          1592380051,
	ExpiryDate:         0,
	ExpireInFavorOfURN: "",
	ExpireInFavorOfID:  0,
	Status:             protocol.Software_PreAlpha,

	Authorization: authorization.Service{
		CRUD:     authorization.CRUDRead,
		UserType: protocol.UserType_All,
	},

	Detail: map[protocol.LanguageID]service.ServiceDetail{
		protocol.LanguageEnglish: {
			Name:        "Approve Person PublicKey",
			Description: "Approve given key if given data valid or return error",
			TAGS:        []string{"Authentication"},
		},
	},

	SRPCHandler: ApprovePersonPublicKeySRPC,
	ServeHTTP:   ApprovePersonPublicKeyHTTP,
}

// ApprovePersonPublicKeySRPC is sRPC handler of ApprovePersonPublicKey service.
func ApprovePersonPublicKeySRPC(st protocol.Stream) {
	var req = &approvePersonPublicKeyReq{}
	err = req.FromSyllab(srpc.GetPayload(st.IncomePayload))
	if err != nil {
		return
	}

	var res *approvePersonPublicKeyRes
	res, err = approvePersonPublicKey(st, req)
	// Check if any error occur in business logic
	if err != nil {
		return
	}

	st.OutcomePayload = make([]byte, srpc.MinLength+res.LenAsSyllab())
	res.ToSyllab(srpc.GetPayload(st.OutcomePayload))
}

// ApprovePersonPublicKeyHTTP is HTTP handler of ApprovePersonPublicKey service.
func ApprovePersonPublicKeyHTTP(st protocol.Stream, httpReq *http.Request, httpRes *http.Response) {
	var req = &approvePersonPublicKeyReq{}
	err = req.FromJSON(httpReq.Body().Marshal())
	if err != nil {
		httpRes.SetStatus(http.StatusBadRequestCode, http.StatusBadRequestPhrase)
		return
	}

	var res *approvePersonPublicKeyRes
	res, err = approvePersonPublicKey(st, req)
	// Check if any error occur in business logic
	if err != nil {
		httpRes.SetStatus(http.StatusBadRequestCode, http.StatusBadRequestPhrase)
		return
	}

	httpRes.SetStatus(http.StatusOKCode, http.StatusOKPhrase)
	httpRes.SetBody(json.NewCodec(res))
}

type approvePersonPublicKeyReq struct {
	PersonID  [32]byte `json:",string"`
	PublicKey [32]byte `json:",string"`
	ThingID   [32]byte `json:",string"`
}

type approvePersonPublicKeyRes struct {
	Status data.PersonPublicKeyStatus
}

func approvePersonPublicKey(st protocol.Stream, req *approvePersonPublicKeyReq) (res *approvePersonPublicKeyRes, err protocol.Error) {
	// TODO::: Authenticate request first by service policy.

	err = st.Authorize()
	if err != nil {
		return
	}

	// Validate data here due to service use internally by other services!
	err = req.validator()
	if err != nil {
		return
	}

	// Just can call by registered org

	res = &approvePersonPublicKeyRes{}

	return
}

func (req *approvePersonPublicKeyReq) validator() (err protocol.Error) {
	return
}

/*
	Request Encoders & Decoders
*/

func (req *approvePersonPublicKeyReq) FromSyllab(payload []byte, stackIndex uint32) {
	return
}

func (req *approvePersonPublicKeyReq) FromJSON(payload []byte) (remaining []byte, err protocol.Error) {
	err = json.Unmarshal(buf, req)
	return
}

/*
	Response Encoders & Decoders
*/

func (res *approvePersonPublicKeyRes) ToSyllab(payload []byte, stackIndex, heapIndex uint32) (freeHeapIndex uint32) {
	syllab.SetUInt8(buf, 0, uint8(res.Status))
}

func (res *approvePersonPublicKeyRes) LenOfSyllabStack() uint32 {
	return 1
}

func (res *approvePersonPublicKeyRes) LenOfSyllabHeap() (ln uint32) {
	return
}

func (res *approvePersonPublicKeyRes) LenAsSyllab() uint64 {
	return uint64(res.LenOfSyllabStack() + res.LenOfSyllabHeap())
}

func (res *approvePersonPublicKeyRes) ToJSON(payload []byte) (added []byte, err protocol.Error) {
	var encoder = json.Encoder{Buf: payload}

	buf, _ = json.Marshal(res)
	return
}
