/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/authorization"
	er "libgo/error"
	"libgo/http"
	"libgo/json"
	"libgo/srpc"
	"libgo/syllab"
	"libgo/uuid"
	"libgo/validators"
)

var registerNewOrganizationService = service.Service{
	URN:                "urn:giti:sabz.city:service:register-organization",
	Domain:             DomainName,
	ID:                 6912182473652264594,
	IssueDate:          1604472315,
	ExpiryDate:         0,
	ExpireInFavorOfURN: "",
	ExpireInFavorOfID:  0,
	Status:             protocol.Software_PreAlpha,

	Authorization: authorization.Service{
		CRUD:     authorization.CRUDCreate,
		UserType: protocol.UserType_Person,
	},

	Name: map[protocol.LanguageID]string{
		protocol.LanguageEnglish: "Register Organization",
	},
	Description: map[protocol.LanguageID]string{
		protocol.LanguageEnglish: "",
	},
	TAGS: []string{
		"OrganizationAuthentication",
	},

	SRPCHandler: RegisterNewOrganizationSRPC,
	ServeHTTP: RegisterNewOrganizationHTTP,
}

// RegisterNewOrganizationSRPC is sRPC handler of RegisterNewOrganization service.
func RegisterNewOrganizationSRPC(st protocol.Stream) {
	var req = &registerNewOrganizationReq{}
	err = req.FromSyllab(srpc.GetPayload(st.IncomePayload))
	if err != nil {
		return
	}

	var res *registerNewOrganizationRes
	res, err = registerNewOrganization(st, req)
	// Check if any error occur in business logic
	if err != nil {
		return
	}

	st.OutcomePayload = make([]byte, srpc.MinLength+res.LenAsSyllab())
	res.ToSyllab(srpc.GetPayload(st.OutcomePayload))
}

// RegisterNewOrganizationHTTP is HTTP handler of RegisterNewOrganization service.
func RegisterNewOrganizationHTTP(st protocol.Stream, httpReq *http.Request, httpRes *http.Response) {
	var req = &registerNewOrganizationReq{}
	err = req.FromJSON(httpReq.Body().Marshal())
	if err != nil {
		httpRes.SetStatus(http.StatusBadRequestCode, http.StatusBadRequestPhrase)
		return
	}

	var res *registerNewOrganizationRes
	res, err = registerNewOrganization(st, req)
	// Check if any error occur in business logic
	if err != nil {
		httpRes.SetStatus(http.StatusBadRequestCode, http.StatusBadRequestPhrase)
		return
	}

	httpRes.SetStatus(http.StatusOKCode, http.StatusOKPhrase)
	httpRes.SetBody(json.NewCodec(res))
}

type registerNewOrganizationReq struct {
	SocietyID    [32]byte
	ServicesType data.OrganizationAuthenticationType

	Language protocol.Language
	Title    string `valid:"OrgName"`
	Domain   string `valid:"Domain"`

	LeaderPersonID [32]byte `json:",string"`
}

type registerNewOrganizationRes struct {
	ID [32]byte `json:",string"`
}

func registerNewOrganization(st protocol.Stream, req *registerNewOrganizationReq) (res *registerNewOrganizationRes, err protocol.Error) {
	if st.Connection.UserID != adminUserID {
		err = authorization.ErrUserNotAllow
		return
	}

	err = st.Authorize()
	if err != nil {
		return
	}
	// Validate data here due to service use internally by other services!
	err = req.validator()
	if err != nil {
		return
	}

	// Check Founder status
	var getPersonStatusReq = getPersonStatusReq{
		PersonID: req.LeaderPersonID,
	}
	var getPersonStatusRes *getPersonStatusRes
	getPersonStatusRes, err = getPersonStatus(st, &getPersonStatusReq, true)
	if err != nil {
		return
	}
	if getPersonStatusRes.Status == data.PersonAuthenticationBlocked {
		err = ErrBlockedPerson
		return
	}

	var oa = data.OrganizationAuthentication{
		AppInstanceID:    achaemenid.App.Nodes.LocalNode.InstanceID,
		UserConnectionID: st.Connection.ID,
		ID:               uuid.Random32Byte(),
		SocietyID:        req.SocietyID,
		ServicesType:     req.ServicesType,
		Status:           data.OrganizationStatusRegister,
	}
	if req.SocietyID == [32]byte{} {
		oa.SocietyID = achaemenid.App.Manifest.SocietyUUID
	} else if req.SocietyID != achaemenid.App.Manifest.SocietyUUID {
		oa.Status = data.OrganizationStatusRepresentative
	}

	if req.Domain != "" {
		err = checkQuiddityURI(st, req.Domain)
		if err != nil {
			return
		}
	}
	var q = data.Quiddity{
		AppInstanceID:    achaemenid.App.Nodes.LocalNode.InstanceID,
		UserConnectionID: st.Connection.ID,
		ID:               uuid.Random32Byte(),
		OrgID:            oa.ID,

		Language: req.Language,
		URI:      req.Domain,
		Title:    req.Title,
		Status:   data.QuiddityStatusRegister,
	}
	err = q.SaveNew()
	if err != nil {
		return
	}

	oa.QuiddityID = q.ID
	err = oa.SaveNew()
	if err != nil {
		return
	}

	// make new connection for leader
	var uac = data.UserAppConnection{
		Status:      data.UserAppConnectionIssued,
		Description: "Leader connection created in register the organization",

		ID: uuid.Random32Byte(),

		// ThingID:          st.Connection.ThingID,
		UserID:           oa.ID,
		UserType:         protocol.UserType_Org,
		DelegateUserID:   req.LeaderPersonID,
		DelegateUserType: st.Connection.UserType,
	}
	uac.AccessControl.GiveFullAccess()
	err = uac.SaveNew()
	if err != nil {
		// TODO::: Can't return easily!!
		return
	}

	res = &registerNewOrganizationRes{
		ID: oa.ID,
	}
	return
}

func (req *registerNewOrganizationReq) validator() (err protocol.Error) {
	err = validators.ValidateText(req.Title, 0, 100)
	err = validators.ValidateText(req.Domain, 0, 100)
	return
}

/*
	Request Encoders & Decoders
*/

func (req *registerNewOrganizationReq) FromSyllab(payload []byte, stackIndex uint32) {
	if uint32(len(buf)) < req.LenOfSyllabStack() {
		err = syllab.ErrShortArrayDecode
		return
	}

	copy(req.SocietyID[:], buf[0:])
	req.ServicesType = data.OrganizationAuthenticationType(syllab.GetUInt8(buf, 32))

	req.Language = protocol.Language(syllab.GetUInt32(buf, 33))
	req.Title = syllab.UnsafeGetString(buf, 37)
	req.Domain = syllab.UnsafeGetString(buf, 45)

	copy(req.LeaderPersonID[:], buf[53:])
	return
}

func (req *registerNewOrganizationReq) ToSyllab(payload []byte, stackIndex, heapIndex uint32) (freeHeapIndex uint32)
	copy(buf[0:], req.SocietyID[:])
	syllab.SetUInt8(buf, 32, uint8(req.ServicesType))

	syllab.SetUInt32(buf, 33, uint32(req.Language))
	heapIndex = syllab.SetString(buf, req.Title, 37, heapIndex)
	heapIndex = syllab.SetString(buf, req.Domain, 45, heapIndex)

	copy(buf[53:], req.LeaderPersonID[:])
	return
}

func (req *registerNewOrganizationReq) LenOfSyllabStack() uint32 {
	return 85
}

func (req *registerNewOrganizationReq) LenOfSyllabHeap() (ln uint32) {
	ln += uint32(len(req.Title))
	ln += uint32(len(req.Domain))
	return
}

func (req *registerNewOrganizationReq) LenAsSyllab() uint64 {
	return uint64(req.LenOfSyllabStack() + req.LenOfSyllabHeap())
}

func (req *registerNewOrganizationReq) FromJSON(payload []byte) (remaining []byte, err protocol.Error) {
	var decoder = json.DecoderUnsafeMinified{Buf: payload}
	for err == nil {
		var keyName = decoder.DecodeKey()
		switch keyName {
		case "SocietyID":
			err = decoder.DecodeByteArrayAsNumber(req.SocietyID[:])
		case "ServicesType":
			var num uint8
			num, err = decoder.DecodeUInt8()
			req.ServicesType = data.OrganizationAuthenticationType(num)

		case "Language":
			var num uint32
			num, err = decoder.DecodeUInt32()
			req.Language = protocol.Language(num)
		case "Title":
			req.Title, err = decoder.DecodeString()
		case "Domain":
			req.Domain, err = decoder.DecodeString()

		case "LeaderPersonID":
			err = decoder.DecodeByteArrayAsBase64(req.LeaderPersonID[:])
		default:
			err = decoder.NotFoundKeyStrict()
		}

		if decoder.End() {
			return
		}
	}
	return
}

func (req *registerNewOrganizationReq) ToJSON(payload []byte) (added []byte, err protocol.Error) {
	var encoder = json.Encoder{Buf: payload}

	encoder.EncodeString(`{"SocietyID":[`)
	encoder.EncodeByteSliceAsNumber(req.SocietyID[:])
	encoder.EncodeString(`],"ServicesType":`)
	encoder.EncodeUInt8(uint8(req.ServicesType))

	encoder.EncodeString(`,"Language":`)
	encoder.EncodeUInt32(uint32(req.Language))
	encoder.EncodeString(`,"Title":"`)
	encoder.EncodeString(req.Title)
	encoder.EncodeString(`","Domain":"`)
	encoder.EncodeString(req.Domain)

	encoder.EncodeString(`","LeaderPersonID":"`)
	encoder.EncodeByteSliceAsBase64(req.LeaderPersonID[:])

	encoder.EncodeByte('}')
	return encoder.Buf
}

func (req *registerNewOrganizationReq) LenAsJSON() (ln int) {
	ln = len(req.Title) + len(req.Domain)
	ln += 271
	return
}

/*
	Response Encoders & Decoders
*/

func (res *registerNewOrganizationRes) FromSyllab(payload []byte, stackIndex uint32) {
	if uint32(len(buf)) < res.LenOfSyllabStack() {
		err = syllab.ErrShortArrayDecode
		return
	}

	copy(res.ID[:], buf[0:])
	return
}

func (res *registerNewOrganizationRes) ToSyllab(payload []byte, stackIndex, heapIndex uint32) (freeHeapIndex uint32)
	copy(buf[0:], res.ID[:])
	return
}

func (res *registerNewOrganizationRes) LenOfSyllabStack() uint32 {
	return 32
}

func (res *registerNewOrganizationRes) LenOfSyllabHeap() (ln uint32) {
	return
}

func (res *registerNewOrganizationRes) LenAsSyllab() uint64 {
	return uint64(res.LenOfSyllabStack() + res.LenOfSyllabHeap())
}

func (res *registerNewOrganizationRes) FromJSON(payload []byte) (remaining []byte, err protocol.Error) {
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

func (res *registerNewOrganizationRes) ToJSON(payload []byte) (added []byte, err protocol.Error) {
	var encoder = json.Encoder{Buf: payload}

	encoder.EncodeString(`{"ID":"`)
	encoder.EncodeByteSliceAsBase64(res.ID[:])

	encoder.EncodeString(`"}`)
	return encoder.Buf
}

func (res *registerNewOrganizationRes) LenAsJSON() (ln int) {
	ln = 52
	return
}
