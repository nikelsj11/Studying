import java.awt.*;
import java.util.*;

import static com.sun.org.apache.xalan.internal.lib.ExsltMath.cos;
import static com.sun.org.apache.xalan.internal.lib.ExsltMath.sin;
import static java.lang.Math.round;
import static java.lang.StrictMath.abs;


// структура для 2х мерной точки
class TPoint2D{
    public double x, y = 0;

    public TPoint2D(double x, double y){
        setPoint(x, y);
    }

    public void setPoint(double x, double y){
        this.x = x;
        this.y = y;
    }
}

// структура для хранения точки в 3х мерном пространстве
class TPoint3D extends TPoint2D{
    public double z = 0;

    public TPoint3D(double x, double y, double z){
        super(x, y);
        this.z = z;
    }
}

// структура для квадратного полигонаы
class TSquare implements Comparable{
    public TPoint2D[] points2D = new TPoint2D[4];
    public TPoint3D[] vertexes = new TPoint3D[4];
    public TPoint3D normal;
    public Color color;
    public TSquare(TPoint3D[] vertexes, TPoint3D normal){
        this.normal = normal;
        this.vertexes = vertexes;
    }

    // метод для сортировки (исп. при прорисовке и освещении)
    @Override public int compareTo(Object obj) {
        TSquare comparable = (TSquare) obj;
        if (this.normal.z<comparable.normal.z)
            return 1;
        else if (this.normal.z>comparable.normal.z)
            return -1;
        return 0;
    }
}

// структура для куба
class TQuad {
    public TSquare[] sides =  new TSquare[6];
    private double factorD, factorOfs, x0, y0;
    private Color color;

    // конструктор
    public TQuad(int clientWidth, int clientHeight){
        this.factorD = this.factorOfs = (clientHeight+clientWidth)/2;
        this.x0 = clientWidth / 2;
        this.y0 = clientHeight / 2;
    }

    // добавление вершины
    public void setSides(double[][][] sides, double[][] normals){
        for(int side_number=0; side_number < sides.length; side_number++){

            TPoint3D[] points = new TPoint3D[sides[side_number].length];

            for(int coordinate = 0; coordinate <sides[side_number].length; coordinate++)
                points[coordinate] = new TPoint3D(sides[side_number][coordinate][0],
                                                  sides[side_number][coordinate][1],
                                                  sides[side_number][coordinate][2]);

            TPoint3D normal = new TPoint3D(normals[side_number][0], normals[side_number][1], normals[side_number][2]);
            this.sides[side_number] = new TSquare(points, normal);
        }

    }

    // поворот по оси XY
    public void rotateXY(double angle){
        double sin_angle = sin(angle);
        double cos_angle = cos(angle);

        for(int i=0; i < sides.length; i++){
            for(int j=0; j < sides[i].vertexes.length; j++){
                sides[i].vertexes[j].x = 1.000005*(sides[i].vertexes[j].x * cos_angle - sides[i].vertexes[j].y * sin_angle);
                sides[i].vertexes[j].y = 1.000005*(sides[i].vertexes[j].x * sin_angle + sides[i].vertexes[j].y * cos_angle);
            }
            sides[i].normal.x = sides[i].normal.x * cos_angle - sides[i].normal.y * sin_angle;
            sides[i].normal.y = sides[i].normal.x * sin_angle + sides[i].normal.y * cos_angle;
        }

    }

    // поворот по оси YZ
    public void rotateYZ(double angle){
        double sin_angle = sin(angle);
        double cos_angle = cos(angle);

        for(int i=0; i < sides.length; i++){
            for(int j=0; j < sides[i].vertexes.length; j++){
                sides[i].vertexes[j].z = 1.000005*(sides[i].vertexes[j].y * sin_angle + sides[i].vertexes[j].z * cos_angle);
                sides[i].vertexes[j].y = 1.000005*(sides[i].vertexes[j].y * cos_angle - sides[i].vertexes[j].z * sin_angle);
            }
            sides[i].normal.z = sides[i].normal.y * sin_angle + sides[i].normal.z * cos_angle;
            sides[i].normal.y = sides[i].normal.y * cos_angle - sides[i].normal.z * sin_angle;
        }
    }

    // поворот по оси XZ
    public void rotateXZ(double angle){
        double sin_angle = sin(angle);
        double cos_angle = cos(angle);

        for(int i=0; i < sides.length; i++){
            for(int j=0; j < sides[i].vertexes.length; j++){
                sides[i].vertexes[j].z = 1.000005*(sides[i].vertexes[j].x * sin_angle + sides[i].vertexes[j].z * cos_angle);
                sides[i].vertexes[j].x = 1.000005*(sides[i].vertexes[j].x * cos_angle - sides[i].vertexes[j].z * sin_angle);
            }
            sides[i].normal.z = sides[i].normal.x * sin_angle + sides[i].normal.z * cos_angle;
            sides[i].normal.x = sides[i].normal.x * cos_angle - sides[i].normal.z * sin_angle;
        }

    }

    // обновление 2D координат
    public void applyChanges(){
        // сортируем массив
        Arrays.sort(sides);



        // новые цвета для каждой из сторон в зависимости от положения нормали
        for(int side = 0; side < sides.length; side++){
            this.sides[side].color =new Color(
                    abs((int)(color.getRed()*-(this.sides[side].normal.z))),
                    abs((int)(color.getGreen()*-(this.sides[side].normal.z))),
                    abs((int)(color.getBlue()*-(this.sides[side].normal.z)))
            );

            // назначаем новые 2D координаты для каждой из точек куба с учетом перспективы
            double perspective;
            for(int item = 0; item < this.sides[side].vertexes.length; item++){
                perspective = this.factorD / (this.sides[side].vertexes[item].z + this.factorOfs);
                this.sides[side].points2D[item] = new TPoint2D(
                        this.x0 + round(this.sides[side].vertexes[item].x * perspective),
                        this.y0 + round(this.sides[side].vertexes[item].y * perspective)
                );
            }


        }
    }

    // обновление 2D координат без перспективы
    public void applyChangesWithoutPerspective(){
        // аналогично только без перспективы
        Arrays.sort(sides);
        for(int side = 0; side < sides.length; side++){
            this.sides[side].color =new Color(
                    abs((int)(color.getRed()*-(this.sides[side].normal.z))),
                    abs((int)(color.getGreen()*-(this.sides[side].normal.z))),
                    abs((int)(color.getBlue()*-(this.sides[side].normal.z)))
            );

            for(int item = 0; item < this.sides[side].vertexes.length; item++){
                this.sides[side].points2D[item] = new TPoint2D(
                        this.x0 + round(this.sides[side].vertexes[item].x),
                        this.y0 + round(this.sides[side].vertexes[item].y)
                );
            }
        }
    }

    // установить цвет куба
    public void setColor(Color color){
        this.color = color;
    }

}
