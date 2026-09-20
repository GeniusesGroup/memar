/* For license and copyright information please see the LEGAL file in the code repository */

package quiddity

import (
	"libgo/authorization"
	"libgo/http"
	"libgo/json"
	"libgo/matn"
	"libgo/protocol"
	"libgo/service"
	"libgo/srpc"
	"libgo/syllab"
)

var findQuiddityByTitleService = service.Service{
	URN:                "urn:giti:sabz.city:service:find-quiddity-by-title",
	Domain:             DomainName,
	ID:                 9541719435486761994,
	IssueDate:          1605026748,
	ExpiryDate:         0,
	ExpireInFavorOfURN: "",
	ExpireInFavorOfID:  0,
	Status:             protocol.Software_PreAlpha,

	Authorization: authorization.Service{
		CRUD:     authorization.CRUDRead,
		UserType: protocol.UserType_All,
	},

	Name: map[protocol.LanguageID]string{
		protocol.LanguageEnglish: "Find Quiddity By Title",
	},
	Description: map[protocol.LanguageID]string{
		protocol.LanguageEnglish: "Find Quiddity IDs by given title",
	},
	TAGS: []string{
		"Quiddity",
	},

	SRPCHandler: FindQuiddityByTitleSRPC,
	ServeHTTP:   FindQuiddityByTitleHTTP,
}

// FindQuiddityByTitleSRPC is sRPC handler of FindQuiddityByTitle service.
func FindQuiddityByTitleSRPC(st protocol.Stream) {
	var req = &findQuiddityByTitleReq{}
	err = req.FromSyllab(srpc.GetPayload(st.IncomePayload))
	if err != nil {
		return
	}

	var res *matn.IndexTextFindRes
	res, err = findQuiddityByTitle(st, req)
	// Check if any error occur in business logic
	if err != nil {
		return
	}

	st.OutcomePayload = make([]byte, res.LenAsSyllab()+4)
	res.ToSyllab(srpc.GetPayload(st.OutcomePayload))
}

// FindQuiddityByTitleHTTP is HTTP handler of FindQuiddityByTitle service.
func FindQuiddityByTitleHTTP(st protocol.Stream, httpReq *http.Request, httpRes *http.Response) {
	var req = &findQuiddityByTitleReq{}
	err = req.FromJSON(httpReq.Body().Marshal())
	if err != nil {
		httpRes.SetStatus(http.StatusBadRequestCode, http.StatusBadRequestPhrase)
		return
	}

	var res *matn.IndexTextFindRes
	res, err = findQuiddityByTitle(st, req)
	// Check if any error occur in business logic
	if err != nil {
		httpRes.SetStatus(http.StatusBadRequestCode, http.StatusBadRequestPhrase)
		return
	}

	httpRes.SetStatus(http.StatusOKCode, http.StatusOKPhrase)
	httpRes.SetBody(json.NewCodec(res))
}

type findQuiddityByTitleReq struct {
	Title      string
	PageNumber uint64
}

func findQuiddityByTitle(st protocol.Stream, req *findQuiddityByTitleReq) (res *matn.IndexTextFindRes, err protocol.Error) {
	var q = data.Quiddity{
		Title: req.Title,
	}
	res, err = q.FindIDsByTitle(req.PageNumber)
	return
}

/*
	Request Encoders & Decoders
*/

func (req *findQuiddityByTitleReq) FromSyllab(payload []byte, stackIndex uint32) {
	if uint32(len(buf)) < req.LenOfSyllabStack() {
		err = syllab.ErrShortArrayDecode
		return
	}

	req.Title = syllab.UnsafeGetString(buf, 0)
	req.PageNumber = syllab.GetUInt64(buf, 8)
	return
}

func (req *findQuiddityByTitleReq) ToSyllab(payload []byte, stackIndex, heapIndex uint32) (freeHeapIndex uint32) {
	heapIndex = syllab.SetString(buf, req.Title, 0, heapIndex)
	syllab.SetUInt64(buf, 8, req.PageNumber)
	return
}

func (req *findQuiddityByTitleReq) LenOfSyllabStack() uint32 {
	return 16
}

func (req *findQuiddityByTitleReq) LenOfSyllabHeap() (ln uint32) {
	ln = uint32(len(req.Title))
	return
}

func (req *findQuiddityByTitleReq) LenAsSyllab() uint64 {
	return uint64(req.LenOfSyllabStack() + req.LenOfSyllabHeap())
}

func (req *findQuiddityByTitleReq) FromJSON(payload []byte) (remaining []byte, err protocol.Error) {
	var decoder = json.DecoderUnsafeMinified{Buf: payload}
	for err == nil {
		var keyName = decoder.DecodeKey()
		switch keyName {
		case "Title":
			req.Title, err = decoder.DecodeString()
		case "PageNumber":
			req.PageNumber, err = decoder.DecodeUInt64()
		default:
			err = decoder.NotFoundKeyStrict()
		}

		if decoder.End() {
			return
		}
	}
	return
}

func (req *findQuiddityByTitleReq) ToJSON(payload []byte) (added []byte, err protocol.Error) {
	var encoder = json.Encoder{Buf: payload}
	encoder.EncodeString(`{"Title":"`)
	encoder.EncodeString(req.Title)
	encoder.EncodeString(`","PageNumber":`)
	encoder.EncodeUInt64(req.PageNumber)
	encoder.EncodeByte('}')
	return encoder.Buf
}

func (req *findQuiddityByTitleReq) LenAsJSON() (ln int) {
	ln = len(req.Title)
	ln += 50
	return
}
