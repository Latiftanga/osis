
    def create(self, validated_data):
        appointment_data = None
        certificates_data = None
        promotions_data = None

        if 'appointment' in validated_data.keys():
            appointment_data = validated_data.pop('appointment')
        if 'certificates' in validated_data.keys():
            certificates_data = validated_data.pop('certificates')
        if 'promotions' in validated_data.keys():
            promotions_data = validated_data.pop('promotions')

        staff = models.Staff.objects.create(
            **validated_data,
        )
        if appointment_data:
            appointment = models.Appointment.objects.create(
                **appointment_data,
            )
            print(appointment_data)
            staff.appointment = appointment


        if certificates_data:
            for qualifications_data in certificate_data:
                models.Certificate.objects.create(
                    staff=staff, 
                    **certificate_data,
                )

        if promotions_data:
            for promotion_data in promotions_data:
                models.Promotion.objects.create(
                    staff=staff,
                    **promotions_data,
                )
        staff.save()
        return staff

    def update(self, instance, validated_data):
        
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.middle_name = validated_data.get('middle_name', instance.middle_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.sex = validated_data.get('sex', instance.sex)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.address = validated_data.get('address', instance.address)
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.sssnit_no = validated_data.get('sssnit_no', instance.sssnit_no)
        instance.created_by = validated_data.get('created_by', instance.created_by)
        instance.save()

        if 'appointment' in validated_data.keys() and instance.appointment:
            appointment_data = validated_data.pop('appointment')
            appointment = instance.appointment

            appointment.category = appointment_data.get('category', appointment.category)
            appointment.job_title = appointment_data.get('job_title', appointment.job_description)
            appointment.job_description = appointment_data.get('job_description', appointment.job_description)
            appointment.date_employed = appointment_data.get('date_employed', appointment.date_employed)
            appointment.staff_id = appointment_data.get('staff_id', appointment.staff_id)
            appointment.registered_no = appointment_data.get('registered_no', appointment.registered_no)
            appointment.grade = appointment_data.get('grade', appointment.grade)
            appointment.created_by = appointment_data.get('updated_by', appointment.updated_by)
            appointment.save()
        return instance




class ProgrammeViewSets(ListCreateReadUpdateViewSet):
    """Programme viewsets"""

    queryset = Programme.objects.all()
    serializer_class = serializers.ProgrammeSerializer

    def get_queryset(self):
        # schools_that_run prog with id1 = Prog.objects.filter(schools__in=[<id1>])
        return self.queryset.filter(schools__id=self.request.user.school.id)

    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save(
            created_by=self.request.user.email
        )
        programme = serializer.save(created_by=self.request.user.email)
        programme.schools.add(self.request.user.school)
        programme.save()

    @action(methods=('POST',), detail=False, url_path='register-programmes')
    def register_programmes(self, request, pk=None):
        """Register programmes the school runs"""

        serializer = self.get_serializer(request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


    @action(methods=('GET', 'POST'), detail=False, url_path='grades')
    def grades(self, request):
        if request.method == 'GET':
            queryset = Grade.objects.all()
            serializer = self.get_serializer(queryset, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'POST':
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save(
                    created_by=self.request.user.email,
                    school=self.request.user.school
                )
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=('GET', 'PUT'), detail=False, url_path='grades/(?P<pk>[^/.]+)')
    def grade(self, request, pk=None):
        if self.request.method == 'GET':
            queryset = Grade.objects.get(pk=self.kwargs['pk'])
            serializer = self.get_serializer(queryset)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif self.request.method == 'PUT':
            serializer = self.get_serializer(request.data)
            if serializer.is_valid():
                serializer.save(
                    updated_by=self.request.user.email,
                    school=self.request.user.school
                )
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)