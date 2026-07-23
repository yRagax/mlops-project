from pydantic import BaseModel, Field


# 1. Define the input schema using Pydantic
class InferenceInput(BaseModel):
    longitude: float = Field(
        ...,
        description="A measure of how far west a house is; a higher value is farther west",
    )
    latitude: float = Field(
        ...,
        description="A measure of how far north a house is; a higher value is farther north",
    )
    housing_median_age: float = Field(
        ...,
        description="Median age of a house within a block; a lower number is a newer building",
    )
    total_rooms: float = Field(..., description="Total number of rooms within a block")
    total_bedrooms: float = Field(
        ..., description="Total number of bedrooms within a block"
    )
    population: float = Field(
        ..., description="Total number of people residing within a block"
    )
    households: float = Field(
        ...,
        description="Total number of households, a group of people residing within a home unit, for a block",
    )
    median_income: float = Field(
        ...,
        description="Median income for households within a block of houses (measured in tens of thousands of US Dollars)",
    )


# 2. Define the output schema
class InferenceOutput(BaseModel):
    prediction: float = Field(..., description="The predicted continuous value")
