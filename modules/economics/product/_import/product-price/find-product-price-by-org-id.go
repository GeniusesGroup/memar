/* For license and copyright information please see the LEGAL file in the code repository */

package pp

import (
	"libgo/authorization"
	"libgo/http"
	"libgo/json"
	"libgo/protocol"
	"libgo/srpc"
	"libgo/syllab"
)

var findProductPriceByOrgIDService = service.Service{
	URN:                "urn:giti:sabz.city:service:find-product-price-by-org-id",
	Domain:             DomainName,
	ID:                 14052467035502513274,
	IssueDate:          1608092848,
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
			Name:        "Find Product Price By Org ID",
			Description: "",
			TAGS:        []string{"ProductPrice"},
		},
	},

	SRPCHandler: FindProductPriceByOrgIDSRPC,
	ServeHTTP:   FindProductPriceByOrgIDHTTP,
}

// FindProductPriceByOrgIDSRPC is sRPC handler of FindProductPriceByOrgID service.
func FindProductPriceByOrgIDSRPC(st protocol.Stream) {
	var req = &findProductPriceByOrgIDReq{}
	err = req.FromSyllab(srpc.GetPayload(st.IncomePayload))
	if err != nil {
		return
	}

	var res *findProductPriceByOrgIDRes
	res, err = findProductPriceByOrgID(st, req)
	// Check if any error occur in business logic
	if err != nil {
		return
	}

	st.OutcomePayload = make([]byte, srpc.MinLength+res.LenAsSyllab())
	res.ToSyllab(srpc.GetPayload(st.OutcomePayload))
}

// FindProductPriceByOrgIDHTTP is HTTP handler of FindProductPriceByOrgID service.
func FindProductPriceByOrgIDHTTP(st protocol.Stream, httpReq *http.Request, httpRes *http.Response) {
	var req = &findProductPriceByOrgIDReq{}
	err = req.FromJSON(httpReq.Body().Marshal())
	if err != nil {
		httpRes.SetStatus(http.StatusBadRequestCode, http.StatusBadRequestPhrase)
		return
	}

	var res *findProductPriceByOrgIDRes
	res, err = findProductPriceByOrgID(st, req)
	// Check if any error occur in business logic
	if err != nil {
		httpRes.SetStatus(http.StatusBadRequestCode, http.StatusBadRequestPhrase)
		return
	}

	httpRes.SetStatus(http.StatusOKCode, http.StatusOKPhrase)
	httpRes.SetBody(json.NewCodec(res))
}

type findProductPriceByOrgIDReq struct {
	OrgID  [32]byte `json:",string"`
	Offset uint64
	Limit  uint64
}

type findProductPriceByOrgIDRes struct {
	QuiddityIDs [][32]byte `json:",string"`
}

func findProductPriceByOrgID(st protocol.Stream, req *findProductPriceByOrgIDReq) (res *findProductPriceByOrgIDRes, err protocol.Error) {
	var pp = data.ProductPrice{
		OrgID: req.OrgID,
	}
	var indexRes [][32]byte
	indexRes, err = pp.FindQuiddityIDsByOrgID(req.Offset, req.Limit)
	if err != nil {
		return
	}

	res = &findProductPriceByOrgIDRes{
		QuiddityIDs: indexRes,
	}
	return
}

/*
	Request Encoders & Decoders
*/

func (req *findProductPriceByOrgIDReq) FromSyllab(payload []byte, stackIndex uint32) {
	if uint32(len(buf)) < req.LenOfSyllabStack() {
		err = syllab.ErrShortArrayDecode
		return
	}

	copy(req.OrgID[:], buf[0:])
	req.Offset = syllab.GetUInt64(buf, 32)
	req.Limit = syllab.GetUInt64(buf, 40)
	return
}

func (req *findProductPriceByOrgIDReq) ToSyllab(payload []byte, stackIndex, heapIndex uint32) (freeHeapIndex uint32) {
	copy(buf[0:], req.OrgID[:])
	syllab.SetUInt64(buf, 32, req.Offset)
	syllab.SetUInt64(buf, 40, req.Limit)
	return
}

func (req *findProductPriceByOrgIDReq) LenOfSyllabStack() uint32 {
	return 48
}

func (req *findProductPriceByOrgIDReq) LenOfSyllabHeap() (ln uint32) {
	return
}

func (req *findProductPriceByOrgIDReq) LenAsSyllab() uint64 {
	return uint64(req.LenOfSyllabStack() + req.LenOfSyllabHeap())
}

func (req *findProductPriceByOrgIDReq) FromJSON(payload []byte) (remaining []byte, err protocol.Error) {
	var decoder = json.DecoderUnsafeMinified{Buf: payload}
	for err == nil {
		var keyName = decoder.DecodeKey()
		switch keyName {
		case "OrgID":
			err = decoder.DecodeByteArrayAsBase64(req.OrgID[:])
		case "Offset":
			req.Offset, err = decoder.DecodeUInt64()
		case "Limit":
			req.Limit, err = decoder.DecodeUInt64()
		default:
			err = decoder.NotFoundKeyStrict()
		}

		if decoder.End() {
			return
		}
	}
	return
}

func (req *findProductPriceByOrgIDReq) ToJSON(payload []byte) (added []byte, err protocol.Error) {
	var encoder = json.Encoder{Buf: payload}
	encoder.EncodeString(`{"OrgID":"`)
	encoder.EncodeByteSliceAsBase64(req.OrgID[:])
	encoder.EncodeString(`","Offset":`)
	encoder.EncodeUInt64(req.Offset)
	encoder.EncodeString(`,"Limit":`)
	encoder.EncodeUInt64(req.Limit)
	encoder.EncodeByte('}')
	return encoder.Buf
}

func (req *findProductPriceByOrgIDReq) LenAsJSON() (ln int) {
	ln = 114
	return
}

/*
	Response Encoders & Decoders
*/

func (res *findProductPriceByOrgIDRes) FromSyllab(payload []byte, stackIndex uint32) {
	if uint32(len(buf)) < res.LenOfSyllabStack() {
		err = syllab.ErrShortArrayDecode
		return
	}

	res.QuiddityIDs = syllab.UnsafeGet32ByteArraySlice(buf, 128)
	return
}

func (res *findProductPriceByOrgIDRes) ToSyllab(payload []byte, stackIndex, heapIndex uint32) (freeHeapIndex uint32) {
	syllab.Set32ByteArrayArray(buf, res.QuiddityIDs, 0, heapIndex)
	return
}

func (res *findProductPriceByOrgIDRes) LenOfSyllabStack() uint32 {
	return 8
}

func (res *findProductPriceByOrgIDRes) LenOfSyllabHeap() (ln uint32) {
	ln = uint32(len(res.QuiddityIDs) * 32)
	return
}

func (res *findProductPriceByOrgIDRes) LenAsSyllab() uint64 {
	return uint64(res.LenOfSyllabStack() + res.LenOfSyllabHeap())
}

func (res *findProductPriceByOrgIDRes) FromJSON(payload []byte) (remaining []byte, err protocol.Error) {
	var decoder = json.DecoderUnsafeMinified{Buf: payload}
	for err == nil {
		var keyName = decoder.DecodeKey()
		switch keyName {
		case "QuiddityIDs":
			res.QuiddityIDs, err = decoder.Decode32ByteArraySliceAsBase64()
		default:
			err = decoder.NotFoundKeyStrict()
		}

		if decoder.End() {
			return
		}
	}
	return
}

func (res *findProductPriceByOrgIDRes) ToJSON(payload []byte) (added []byte, err protocol.Error) {
	var encoder = json.Encoder{Buf: payload}

	encoder.EncodeString(`{"QuiddityIDs":[`)
	encoder.Encode32ByteArraySliceAsBase64(res.QuiddityIDs)

	encoder.EncodeString(`]}`)
}

func (res *findProductPriceByOrgIDRes) LenAsJSON() (ln int) {
	ln = len(res.QuiddityIDs) * 46
	ln += 14
	return
}
