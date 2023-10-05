from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Vendor, Meal, Menu, Review, MealReview
from .serializers import VendorSerializer, MealSerializer, MenuSerializer, ReviewSerializer, MealReviewSerializer


class VendorAPIView(APIView):

    def get(self, request, pk=None):

        if pk is not None:
            try:
                vendor = Vendor.objects.get(pk=pk)
                serializer = VendorSerializer(vendor)
                return Response(serializer.data)
            except Vendor.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data)

    def post(self, request):

        serializer = VendorSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):

        vendor = Vendor.objects.get(pk=pk)
        serializer = VendorSerializer(vendor, data=request.data)

        if serializer.is_valid():
            serializer.save()
            msg = "Complete data updated successfully."
            return Response({'msg': msg}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):

        vendor = Vendor.objects.get(pk=pk)
        serializer = VendorSerializer(vendor, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            msg = "Partial data updated successfully."
            return Response({'msg': msg}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):

        vendor = Vendor.objects.get(pk=pk)
        vendor.delete()
        msg = "Delete vendor successfully."
        return Response({'msg': msg}, status=status.HTTP_204_NO_CONTENT)


class MealAPIView(APIView):

    def get(self, request, pk=None):

        if pk is not None:
            try:
                meal = Meal.objects.get(pk=pk)
                serializer = MealSerializer(meal)
                return Response(serializer.data)
            except Meal.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

        meals = Meal.objects.all()
        serializer = MealSerializer(meals, many=True)
        return Response(serializer.data)

    def post(self, request):

        serializer = MealSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):

        meal = Meal.objects.get(pk=pk)
        serializer = MealSerializer(meal, data=request.data)

        if serializer.is_valid():
            serializer.save()
            msg = "data updated successfully."
            return Response({'msg': msg}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):

        meal = Meal.objects.get(pk=pk)
        serializer = MealSerializer(meal, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            msg = "Partial data updated successfully."
            return Response({'msg': msg}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):

        meal = Meal.objects.get(pk=pk)
        meal.delete()
        msg = "Delete meal successfully."
        return Response({'msg': msg}, status=status.HTTP_204_NO_CONTENT)


class MenuAPIView(APIView):

    def get(self, request, pk=None):

        if pk is not None:
            try:
                menu = Menu.objects.get(pk=pk)
                serializer = MenuSerializer(menu)
                return Response(serializer.data)
            except Menu.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

        menus = Menu.objects.all()
        serializer = MenuSerializer(menus, many=True)
        return Response(serializer.data)

    def post(self, request):

        serializer = MenuSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):

        menu = Menu.objects.get(pk=pk)
        serializer = MenuSerializer(menu, data=request.data)

        if serializer.is_valid():
            serializer.save()
            msg = "data updated successfully."
            return Response({'msg': msg}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):

        menu = Menu.objects.get(pk=pk)
        serializer = MenuSerializer(menu, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            msg = "Partial data updated successfully."
            return Response({'msg': msg}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):

        menu = Menu.objects.get(pk=pk)
        menu.delete()
        msg = "Delete menu successfully."
        return Response({'msg': msg}, status=status.HTTP_204_NO_CONTENT)


class ReviewAPIView(APIView):

    def get(self, request, pk=None):

        if pk is not None:
            try:
                review = Review.objects.get(pk=pk)
                serializer = ReviewSerializer(review)
                return Response(serializer.data)
            except Review.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def post(self, request):

        serializer = ReviewSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):

        review = Review.objects.get(pk=pk)
        serializer = ReviewSerializer(review, data=request.data)

        if serializer.is_valid():
            serializer.save()
            msg = "data updated successfully."
            return Response({'msg': msg}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):

        review = Review.objects.get(pk=pk)
        serializer = ReviewSerializer(review, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            msg = "Partial data updated successfully."
            return Response({'msg': msg}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):

        review = Review.objects.get(pk=pk)
        review.delete()
        msg = "Delete review successfully."
        return Response({'msg': msg}, status=status.HTTP_204_NO_CONTENT)


class MealReviewAPIView(APIView):

    def get(self, request):

        meal_reviews = MealReview.objects.all()
        serializer = MealReviewSerializer(meal_reviews, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):

        user_id = request.data.get('user')
        meal_id = request.data.get('meal')
        review_data = request.data.get('review')

        existing_review = MealReview.objects.filter(user_id=user_id, meal_id=meal_id).first()

        if existing_review:
            review_serializer = ReviewSerializer(existing_review.review, data=review_data)

            if review_serializer.is_valid():
                review_serializer.save()
                msg = "MealReview updated successfully."
                return Response({'msg': msg}, status=status.HTTP_200_OK)
            else:
                return Response(review_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        review_serializer = ReviewSerializer(data=review_data)

        if review_serializer.is_valid():
            review = review_serializer.save()
        else:
            return Response(review_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        meal_review = MealReview.objects.create(
            user_id=user_id,
            meal_id=meal_id,
            review=review
        )

        msg = "MealReview created successfully."

        return Response({'msg': msg}, status=status.HTTP_201_CREATED)
