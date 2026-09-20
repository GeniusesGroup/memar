/* For license and copyright information please see the LEGAL file in the code repository */

package quiddity

import (
	"libgo/achaemenid"
	"libgo/authorization"
	"libgo/ganjine"
	"libgo/http"
	"libgo/json"
	"libgo/protocol"
	"libgo/service"
	"libgo/srpc"
	"libgo/syllab"
	"libgo/uuid"
	"libgo/validators"
)

var registerQuiddityService = service.Service{
	URN:                "urn:giti:sabz.city:service:register-quiddity",
	Domain:             DomainName,
	ID:                 6528426075931204671,
	IssueDate:          1604939795,
	ExpiryDate:         0,
	ExpireInFavorOfURN: "",
	ExpireInFavorOfID:  0,
	Status:             protocol.Software_PreAlpha,

	Authorization: authorization.Service{
		CRUD:     authorization.CRUDCreate,
		UserType: protocol.UserType_Org,
	},

	Name: map[protocol.LanguageID]string{
		protocol.LanguageEnglish: "Register Quiddity",
	},
	Description: map[protocol.LanguageID]string{
		protocol.LanguageEnglish: "",
	},
	TAGS: []string{
		"Quiddity",
	},

	SRPCHandler: RegisterQuidditySRPC,
	ServeHTTP:   RegisterQuiddityHTTP,
}

// RegisterQuidditySRPC is sRPC handler of RegisterQuiddity service.
func RegisterQuidditySRPC(st protocol.Stream) {
	var req = &registerQuiddityReq{}
	err = req.FromSyllab(srpc.GetPayload(st.IncomePayload))
	if err != nil {
		return
	}

	var res *registerQuiddityRes
	res, err = registerQuiddity(st, req)
	// Check if any error occur in business logic
	if err != nil {
		return
	}

	st.OutcomePayload = make([]byte, srpc.MinLength+res.LenAsSyllab())
	res.ToSyllab(srpc.GetPayload(st.OutcomePayload))
}

// RegisterQuiddityHTTP is HTTP handler of RegisterQuiddity service.
func RegisterQuiddityHTTP(st protocol.Stream, httpReq *http.Request, httpRes *http.Response) {
	var req = &registerQuiddityReq{}
	err = req.FromJSON(httpReq.Body().Marshal())
	if err != nil {
		httpRes.SetStatus(http.StatusBadRequestCode, http.StatusBadRequestPhrase)
		return
	}

	var res *registerQuiddityRes
	res, err = registerQuiddity(st, req)
	// Check if any error occur in business logic
	if err != nil {
		httpRes.SetStatus(http.StatusBadRequestCode, http.StatusBadRequestPhrase)
		return
	}

	httpRes.SetStatus(http.StatusOKCode, http.StatusOKPhrase)
	httpRes.SetBody(json.NewCodec(res))
}

type registerQuiddityReq struct {
	Language protocol.Language
	URI      string `valid:"text[0:100]"`
	Title    string `valid:"text[0:100]"`
}

type registerQuiddityRes struct {
	ID [32]byte `json:",string"`
}

func registerQuiddity(st protocol.Stream, req *registerQuiddityReq) (res *registerQuiddityRes, err protocol.Error) {
	err = st.Authorize()
	if err != nil {
		return
	}
	// Validate data here due to service use internally by other services!
	err = req.validator()
	if err != nil {
		return
	}

	if req.URI != "" {
		err = checkQuiddityURI(st, req.URI)
		if err != nil {
			return
		}
	}

	// err = checkOrgName(st, req.Name)
	// if err != nil {
	// 	return
	// }
	// err = checkOrgDomain(st, req.Domain)
	// if err != nil {
	// 	return
	// }

	var q = Quiddity{
		AppInstanceID:    achaemenid.App.Nodes.LocalNode.InstanceID,
		UserConnectionID: st.Connection.ID,
		ID:               uuid.Random32Byte(),
		OrgID:            st.Connection.UserID,

		Language: req.Language,
		URI:      req.URI,
		Title:    req.Title,
		Status:   data.QuiddityStatusRegister,
	}
	err = storage.Save(&q)
	if err != nil {
		return
	}

	res = &registerQuiddityRes{
		ID: q.ID,
	}

	return
}

func (req *registerQuiddityReq) validator() (err protocol.Error) {
	// Title must not include ':'(use in URI)
	err = validators.ValidateText(req.Title, 0, 100)
	err = validators.ValidateText(req.URI, 0, 100)
	return
}

func checkQuiddityURI(st protocol.Stream, uri string) (err protocol.Error) {
	var findQuiddityByURIReq = findQuiddityByURIReq{
		URI:    uri,
		Offset: 18446744073709551615,
		Limit:  1,
	}
	var findQuiddityByURIRes *findQuiddityByURIRes
	findQuiddityByURIRes, err = findQuiddityByURI(st, &findQuiddityByURIReq)
	if err.Equal(ganjine.ErrRecordNotFound) {
		return nil
	}
	if err != nil {
		return
	}

	var getQuiddityLanguagesReq = getQuiddityLanguagesReq{
		ID: findQuiddityByURIRes.IDs[0],
	}
	var getQuiddityLanguagesRes *getQuiddityLanguagesRes
	getQuiddityLanguagesRes, err = getQuiddityLanguages(st, &getQuiddityLanguagesReq)
	if err.Equal(ganjine.ErrRecordNotFound) {
		// TODO::: how it is possible???
		return nil
	}
	if err != nil {
		return
	}

	var getQuiddityReq = getQuiddityReq{
		ID:       findQuiddityByURIRes.IDs[0],
		Language: getQuiddityLanguagesRes.Languages[0],
	}
	var getQuiddityRes *getQuiddityRes
	getQuiddityRes, err = getQuiddity(st, &getQuiddityReq)
	if err.Equal(ganjine.ErrRecordNotFound) {
		// TODO::: how it is possible???
		return nil
	}
	if err != nil {
		return
	}
	if getQuiddityRes.URI == uri {
		return ErrQuiddityURIRegistered
	}
	return
}

/*
	Request Encoders & Decoders
*/

func (req *registerQuiddityReq) FromSyllab(payload []byte, stackIndex uint32) {
	if uint32(len(buf)) < req.LenOfSyllabStack() {
		err = syllab.ErrShortArrayDecode
		return
	}

	req.Language = protocol.Language(syllab.GetUInt32(buf, 0))
	req.URI = syllab.UnsafeGetString(buf, 4)
	req.Title = syllab.UnsafeGetString(buf, 12)
	return
}

func (req *registerQuiddityReq) ToSyllab(payload []byte, stackIndex, heapIndex uint32) (freeHeapIndex uint32) {
	syllab.SetUInt32(buf, 0, uint32(req.Language))
	heapIndex = syllab.SetString(buf, req.URI, 4, heapIndex)
	heapIndex = syllab.SetString(buf, req.Title, 12, heapIndex)
	return
}

func (req *registerQuiddityReq) LenOfSyllabStack() uint32 {
	return 20
}

func (req *registerQuiddityReq) LenOfSyllabHeap() (ln uint32) {
	ln += uint32(len(req.URI))
	ln += uint32(len(req.Title))
	return
}

func (req *registerQuiddityReq) LenAsSyllab() uint64 {
	return uint64(req.LenOfSyllabStack() + req.LenOfSyllabHeap())
}

func (req *registerQuiddityReq) FromJSON(payload []byte) (remaining []byte, err protocol.Error) {
	var decoder = json.DecoderUnsafeMinified{Buf: payload}
	for err == nil {
		var keyName = decoder.DecodeKey()
		switch keyName {
		case "Language":
			var num uint32
			num, err = decoder.DecodeUInt32()
			req.Language = protocol.Language(num)
		case "URI":
			req.URI, err = decoder.DecodeString()
		case "Title":
			req.Title, err = decoder.DecodeString()
		default:
			err = decoder.NotFoundKeyStrict()
		}

		if decoder.End() {
			return
		}
	}
	return
}

func (req *registerQuiddityReq) ToJSON(payload []byte) (added []byte, err protocol.Error) {
	var encoder = json.Encoder{Buf: payload}

	encoder.EncodeString(`{"Language":`)
	encoder.EncodeUInt32(uint32(req.Language))

	encoder.EncodeString(`,"URI":"`)
	encoder.EncodeString(req.URI)

	encoder.EncodeString(`","Title":"`)
	encoder.EncodeString(req.Title)

	encoder.EncodeString(`"}`)
	return encoder.Buf
}

func (req *registerQuiddityReq) LenAsJSON() (ln int) {
	ln = len(req.URI) + len(req.Title)
	ln += 43
	return
}

/*
	Response Encoders & Decoders
*/

func (res *registerQuiddityRes) FromSyllab(payload []byte, stackIndex uint32) {
	if uint32(len(buf)) < res.LenOfSyllabStack() {
		err = syllab.ErrShortArrayDecode
		return
	}

	copy(res.ID[:], buf[0:])
	return
}

func (res *registerQuiddityRes) ToSyllab(payload []byte, stackIndex, heapIndex uint32) (freeHeapIndex uint32) {
	copy(buf[0:], res.ID[:])
	return
}

func (res *registerQuiddityRes) LenOfSyllabStack() uint32 {
	return 32
}

func (res *registerQuiddityRes) LenOfSyllabHeap() (ln uint32) {
	return
}

func (res *registerQuiddityRes) LenAsSyllab() uint64 {
	return uint64(res.LenOfSyllabStack() + res.LenOfSyllabHeap())
}

func (res *registerQuiddityRes) FromJSON(payload []byte) (remaining []byte, err protocol.Error) {
	var decoder = json.DecoderUnsafeMinified{Buf: payload}
	for err == nil {
		var keyName = decoder.DecodeKey()
		switch keyName {
		case "ID":
			err = decoder.DecodeByteArrayAsBase64(res.ID[:])
		default:
			err = decoder.NotFoundKeyStrict()
		}

		if decoder.End() {
			return
		}
	}
	return
}

func (res *registerQuiddityRes) ToJSON(payload []byte) (added []byte, err protocol.Error) {
	var encoder = json.Encoder{Buf: payload}

	encoder.EncodeString(`{"ID":"`)
	encoder.EncodeByteSliceAsBase64(res.ID[:])

	encoder.EncodeString(`"}`)
	return encoder.Buf
}

func (res *registerQuiddityRes) LenAsJSON() (ln int) {
	ln = 52
	return
}
