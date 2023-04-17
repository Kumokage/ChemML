import uuid

from django.db import models


class Thing(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        indexes = [models.Index(fields=["id"])]
        verbose_name = "Объект"
        verbose_name_plural = "Объекты"


class UnitOfMeasure(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        indexes = [models.Index(fields=["id"])]
        verbose_name = "Еденица измерения"
        verbose_name_plural = "Еденицы измерения"


class AbstractProperty(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, verbose_name="Название")
    unit_of_measure = models.ForeignKey(
        UnitOfMeasure,
        on_delete=models.RESTRICT,
        related_name="abstract_properties",
        verbose_name="Еденица измерения",
    )

    class Meta:
        indexes = [models.Index(fields=["id"])]
        verbose_name = "Абстрактное свойство"
        verbose_name_plural = "Абстрактные свойства"


class ChemicalElement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    thing = models.OneToOneField(
        Thing,
        on_delete=models.RESTRICT,
        related_name="chemical_element",
        unique=True,
        verbose_name="Объект",
    )

    class Meta:
        indexes = [models.Index(fields=["id"])]
        verbose_name = "Химический элемент"
        verbose_name_plural = "Химические элементы"


class ChemicalProperty(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    abstract_propery = models.OneToOneField(
        AbstractProperty,
        on_delete=models.RESTRICT,
        related_name="chemical_property",
        unique=True,
        verbose_name="Абстрактное свойство",
    )

    class Meta:
        indexes = [models.Index(fields=["id"])]
        verbose_name = "Химическое свойство"
        verbose_name_plural = "Химические свойства"


class BacterialProperty(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    abstract_propery = models.OneToOneField(
        AbstractProperty,
        on_delete=models.RESTRICT,
        related_name="bacterial_property",
        unique=True,
        verbose_name="Абстрактное свойство",
    )

    class Meta:
        indexes = [models.Index(fields=["id"])]
        verbose_name = "Свойство бактерий"
        verbose_name_plural = "Свойства бактерий"


class Bacteria(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    thing = models.OneToOneField(
        Thing,
        on_delete=models.RESTRICT,
        related_name="bacteria",
        unique=True,
        verbose_name="Объект",
    )
    properties = models.ManyToManyField(
        BacterialProperty, related_name="bacterias", verbose_name="Свойства бактерий"
    )

    class Meta:
        indexes = [models.Index(fields=["id"])]
        verbose_name = "Бактерия"
        verbose_name_plural = "Бактерии"


class ChemicalCompound(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    thing = models.OneToOneField(
        Thing,
        on_delete=models.RESTRICT,
        related_name="chemical_compounds",
        unique=True,
        verbose_name="Объект",
    )
    properties = models.ManyToManyField(
        ChemicalProperty, related_name="chemicals", verbose_name="Свойства химикатов"
    )
    chemical_elements = models.ManyToManyField(
        ChemicalElement,
        related_name="chemicalCompounds",
        verbose_name="Химические элементы",
    )

    class Meta:
        indexes = [models.Index(fields=["id"])]
        verbose_name = "Химическое соединение"
        verbose_name_plural = "Химические соединения"


class DataSet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    properties = models.ManyToManyField(
        AbstractProperty, related_name="datasets", verbose_name="Свойства"
    )
    objects = models.ManyToManyField(
        Thing, related_name="datasets", verbose_name="Объекты"
    )

    class Meta:
        indexes = [models.Index(fields=["id"])]
        verbose_name = "Набор данных"
        verbose_name_plural = "Наборы данных"


class TrainDS(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dataset = models.OneToOneField(
        DataSet, related_name="traindses", verbose_name="Набор данных"
    )

    class Meta:
        indexes = [models.Index(fields=["id"])]
        verbose_name = "Тренировочный набор данных"
        verbose_name_plural = "Тренировочные наборы данных"


class TestDS(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dataset = models.OneToOneField(
        DataSet, related_name="testdses", verbose_name="Набор данных"
    )

    class Meta:
        indexes = [models.Index(fields=["id"])]
        verbose_name = "Тестовый набор данных"
        verbose_name_plural = "Тестовые наборы данных"


class MLModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    train = models.ForeignKey(
        TrainDS,
        on_delete=models.RESTRICT,
        related_name="MLModels",
        verbose_name="Тренировочный набор данных",
    )
    test = models.ForeignKey(
        TestDS,
        on_delete=models.RESTRICT,
        related_name="MLModels",
        verbose_name="Тестовый набор данных",
    )

    class Meta:
        indexes = [models.Index(fields=["id"])]
        verbose_name = "Модель машинного обучения"
        verbose_name_plural = "Модели машинного обучения"


class ComputationalExperiment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    model = models.ForeignKey(
        MLModel,
        on_delete=models.RESTRICT,
        related_name="computational_experiments",
        verbose_name="Модель",
    )

    class Meta:
        indexes = [models.Index(fields=["id"])]
        verbose_name = "Вычислительный эксперимент"
        verbose_name_plural = "Вычислительные эксперименты"


class ComputationalEnvironment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        indexes = [models.Index(fields=["id"])]
        verbose_name = "Вычислительная среда"
        verbose_name_plural = "Вычислительные среды"


class ComputationalExperimentRun(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    venv = models.ForeignKey(
        ComputationalEnvironment,
        on_delete=models.RESTRICT,
        related_name="computational_experiment",
        verbose_name="Вычислительная среда",
    )
    experiment = models.ForeignKey(
        ComputationalExperiment,
        on_delete=models.RESTRICT,
        related_name="runs",
        verbose_name="Эксперимент",
    )

    class Meta:
        indexes = [models.Index(fields=["id"])]
        verbose_name = "Запуск вычислительного эксперимента"
        verbose_name_plural = "Запуски вычислительного эксперимента"


class FieldExperiment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        indexes = [models.Index(fields=["id"])]
        verbose_name = "Эксперимент"
        verbose_name_plural = "Эксперименты"


class Affects(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    field_experiment = models.ForeignKey(
        FieldExperiment,
        on_delete=models.RESTRICT,
        related_name="affect",
        verbose_name="Эксперимент",
    )
    bacteria = models.ForeignKey(
        Bacteria,
        on_delete=models.RESTRICT,
        related_name="affect",
        verbose_name="Бактерия",
    )
    chemical_compound = models.ForeignKey(
        ChemicalCompound,
        on_delete=models.RESTRICT,
        related_name="affects",
        verbose_name="Химическое вещество",
    )
    bacterial_property = models.ForeignKey(
        BacterialProperty,
        on_delete=models.RESTRICT,
        related_name="affects",
        verbose_name="Свойство бактерии",
    )

    class Meta:
        indexes = [models.Index(fields=["id"])]
        verbose_name = "Влияние на бактерии"
        verbose_name_plural = "Влияния на бактерии"


class AffectsByPrediction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bacteria = models.ForeignKey(
        Bacteria,
        on_delete=models.RESTRICT,
        related_name="affect_prediction",
        verbose_name="Бактерия",
    )
    chemical_compound = models.ForeignKey(
        ChemicalCompound,
        on_delete=models.RESTRICT,
        related_name="affect_prediction",
        verbose_name="Химическое вещество",
    )
    bacterial_property = models.ForeignKey(
        BacterialProperty,
        on_delete=models.RESTRICT,
        related_name="affect_prediction",
        verbose_name="Свойство бактерии",
    )
    computational_experiment_run = models.ForeignKey(
        ComputationalExperimentRun,
        on_delete=models.RESTRICT,
        related_name="affects_prediction",
        verbose_name="Запуск вычислительного эксперимента"
    )

    class Meta:
        indexes = [models.Index(fields=["id"])]
        verbose_name = "Прогнозируемое влияние на бактерии"
        verbose_name_plural = "Прогнозируемые влияния на бактерии"
